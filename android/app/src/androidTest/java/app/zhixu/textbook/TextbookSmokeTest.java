package app.zhixu.textbook;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;
import org.json.JSONObject;
import org.json.JSONTokener;
import java.io.File;
import java.io.FileOutputStream;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/** Platform-only instrumentation smoke tests. Run on an emulator/test device, not a personal installation. */
public final class TextbookSmokeTest extends Instrumentation {
    private static final String RECORD_KEY = "zhixu-learning-v1";
    private static final String LESSON = "calculus-03";
    private static final int TOTAL = 6;
    private Activity reader;
    private WebView web;
    private int number;
    private int failures;
    private String originalRecord;
    private boolean capturedRecord;
    private final StringBuilder report = new StringBuilder();

    @Override public void onCreate(Bundle arguments) {
        super.onCreate(arguments);
        start();
    }

    @Override public void onStart() {
        super.onStart();
        try {
            launchReader();
            waitUntil("window.ZHIXU && window.ZHIXU.all.length === 182", "182 lessons did not become ready");
            Object original = evaluate("localStorage.getItem('" + RECORD_KEY + "')");
            originalRecord = original instanceof String ? (String) original : null;
            capturedRecord = true;
            runCase("noDangerousPermissions", this::permissions);
            runCase("localOriginOnly", this::origins);
            runCase("readerAndFormulas", this::formulas);
            runCase("invalidRouteIsSafe", this::invalidRoute);
            runCase("backupRoundTripAndInjection", this::backups);
            runCase("notesSurviveRelaunch", this::relaunch);
        } catch (Throwable failure) {
            failures++;
            report.append("SETUP: ").append(failure.toString()).append('\n');
        } finally {
            if (capturedRecord && reader != null && !reader.isDestroyed()) {
                try {
                    // Reset in-memory state as well as storage so Activity.onPause cannot rewrite test data.
                    String original = originalRecord == null ? "null" : JSONObject.quote(originalRecord);
                    evaluate("(function(){var value=" + original + ";var restored=window.LearningState.normalize(value?JSON.parse(value):null,window.ZHIXU.all);Object.keys(window.ZHIXU.state).forEach(function(k){delete window.ZHIXU.state[k]});Object.assign(window.ZHIXU.state,restored);if(value===null)localStorage.removeItem('" + RECORD_KEY + "');else localStorage.setItem('" + RECORD_KEY + "',value);return true})()");
                } catch (Throwable failure) {
                    failures++;
                    report.append("CLEANUP: ").append(failure.toString()).append('\n');
                }
            }
            if (reader != null) runOnMainSync(() -> reader.finish());
            Bundle result = new Bundle();
            result.putInt("tests", number);
            result.putInt("failures", failures);
            result.putString("stream", "\n" + report + "Tests: " + number + "; failures: " + failures + "\n"
                + (failures == 0 && number == TOTAL ? "ZHIXU_SMOKE_SUCCESS\n" : "ZHIXU_SMOKE_FAILED\n"));
            finish(failures == 0 ? Activity.RESULT_OK : Activity.RESULT_CANCELED, result);
        }
    }

    private interface Check { void run() throws Exception; }

    private void runCase(String name, Check check) {
        number++;
        Bundle status = new Bundle();
        status.putString("class", getClass().getName());
        status.putString("test", name);
        status.putInt("numtests", TOTAL);
        status.putInt("current", number);
        status.putString("id", "ZhixuOfflineSmoke");
        sendStatus(1, status);
        try {
            check.run();
            status.putString("stream", ".");
            sendStatus(0, status);
            report.append("PASS ").append(name).append('\n');
        } catch (Throwable failure) {
            failures++;
            status.putString("stack", failure.toString());
            status.putString("stream", "\nFAIL " + name + ": " + failure + "\n");
            sendStatus(-2, status);
            report.append("FAIL ").append(name).append(": ").append(failure).append('\n');
        }
    }

    private void launchReader() {
        Intent intent = new Intent(getTargetContext(), MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        reader = startActivitySync(intent);
        waitForIdleSync();
        runOnMainSync(() -> web = findWebView(reader.findViewById(android.R.id.content)));
        require(web != null, "WebView missing");
    }

    private static WebView findWebView(View view) {
        if (view instanceof WebView) return (WebView) view;
        if (view instanceof ViewGroup) {
            ViewGroup parent = (ViewGroup) view;
            for (int i = 0; i < parent.getChildCount(); i++) {
                WebView found = findWebView(parent.getChildAt(i));
                if (found != null) return found;
            }
        }
        return null;
    }

    private Object evaluate(String script) throws Exception {
        CountDownLatch completed = new CountDownLatch(1);
        AtomicReference<String> value = new AtomicReference<>();
        runOnMainSync(() -> web.evaluateJavascript(script, result -> {
            value.set(result);
            completed.countDown();
        }));
        require(completed.await(15, TimeUnit.SECONDS), "JavaScript callback timed out");
        String raw = value.get();
        return raw == null ? JSONObject.NULL : new JSONTokener(raw).nextValue();
    }

    private void waitUntil(String expression, String failure) throws Exception {
        long until = SystemClock.uptimeMillis() + 30_000;
        while (SystemClock.uptimeMillis() < until) {
            if (Boolean.TRUE.equals(evaluate("Boolean(" + expression + ")"))) return;
            SystemClock.sleep(150);
        }
        throw new AssertionError(failure);
    }

    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    @SuppressWarnings("deprecation")
    private void permissions() throws Exception {
        PackageInfo info = getTargetContext().getPackageManager().getPackageInfo(
            getTargetContext().getPackageName(), PackageManager.GET_PERMISSIONS);
        String[] requested = info.requestedPermissions == null ? new String[0] : info.requestedPermissions;
        for (String dangerous : new String[]{"android.permission.INTERNET", "android.permission.READ_EXTERNAL_STORAGE",
                "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.CAMERA", "android.permission.RECORD_AUDIO"})
            require(!Arrays.asList(requested).contains(dangerous), "Unexpected permission " + dangerous);
        require(Boolean.TRUE.equals(evaluate("typeof window.Android === 'undefined'")), "Legacy JS interface unexpectedly exposed");
    }

    private void origins() throws Exception {
        Method guard = MainActivity.class.getDeclaredMethod("isLocalAsset", Uri.class);
        guard.setAccessible(true);
        require(Boolean.TRUE.equals(guard.invoke(null, Uri.parse("https://appassets.androidplatform.net/assets/www/index.html#/course/calculus"))), "Valid offline origin rejected");
        for (String blocked : new String[]{"http://appassets.androidplatform.net/assets/www/index.html",
                "https://appassets.androidplatform.net.evil.example/assets/www/index.html",
                "https://evil.example/assets/www/index.html", "file:///android_asset/www/index.html",
                "https://user@appassets.androidplatform.net/assets/www/index.html",
                "https://appassets.androidplatform.net/assets/www/%2e%2e/secret",
                "https://appassets.androidplatform.net/assets/other/index.html"})
            require(Boolean.FALSE.equals(guard.invoke(null, Uri.parse(blocked))), "Unsafe origin allowed " + blocked);
        require(Boolean.TRUE.equals(evaluate("location.origin === 'https://appassets.androidplatform.net'")), "Reader origin incorrect");
    }

    private void formulas() throws Exception {
        require(Boolean.TRUE.equals(evaluate("['exportBackup','importBackup','flush','handleBack'].every(function(k){return typeof window.ZHIXU[k]==='function'})")), "Native app functions missing");
        require(Boolean.TRUE.equals(evaluate("window.ZhixuAndroid && window.ZhixuAndroid.isApp")), "Android adapter missing");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text') && document.querySelectorAll('.katex').length > 10", "Formula lesson failed to render");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0")), "Formula rendering errors");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.teaching-figure img').length>0")), "Diagram missing");
        saveReaderScreenshot();
    }

    private void saveReaderScreenshot() throws Exception {
        CountDownLatch visualReady = new CountDownLatch(1);
        runOnMainSync(() -> web.postVisualStateCallback(SystemClock.uptimeMillis(), new WebView.VisualStateCallback() {
            @Override public void onComplete(long requestId) { visualReady.countDown(); }
        }));
        require(visualReady.await(15, TimeUnit.SECONDS), "Reader visual frame timed out");
        // The callback guarantees readiness for the next draw; allow the compositor to present it.
        SystemClock.sleep(300);
        android.app.UiAutomation automation = getUiAutomation();
        require(automation != null, "Screenshot automation unavailable");
        Bitmap screenshot = automation.takeScreenshot();
        require(screenshot != null, "Reader screenshot unavailable");
        File destination = new File(getTargetContext().getFilesDir(), "reader-screen.png");
        try (FileOutputStream output = new FileOutputStream(destination)) {
            require(screenshot.compress(Bitmap.CompressFormat.PNG, 100, output), "Reader screenshot encoding failed");
            output.flush();
        } finally {
            screenshot.recycle();
        }
    }

    private void invalidRoute() throws Exception {
        evaluate("window.__smokeError=0;window.addEventListener('error',function(){window.__smokeError++});location.hash='#/labs/__proto__'");
        waitUntil("document.querySelector('.labs-index')", "Invalid laboratory route broke the page");
        require(Boolean.TRUE.equals(evaluate("window.__smokeError===0")), "Invalid route raised an error");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text')", "Could not return to lesson");
    }

    private void backups() throws Exception {
        String raw = (String) evaluate("window.ZHIXU.exportBackup()");
        JSONObject backup = new JSONObject(raw);
        require("zhixu-learning".equals(backup.getString("format")), "Backup format missing");
        require(backup.getInt("version") == 1, "Backup version incorrect");
        String dangerousNote = "SMOKE_NOTE <img src=x onerror=window.__noteExecuted=1> </script> \" quote \\ backslash \u2028 line";
        JSONObject noteOnly = new JSONObject();
        noteOnly.put("format", "zhixu-learning");
        noteOnly.put("version", 1);
        noteOnly.put("completed", new org.json.JSONArray());
        noteOnly.put("bookmarks", new org.json.JSONArray());
        noteOnly.put("notes", new JSONObject().put(LESSON, dangerousNote));
        JSONObject result = (JSONObject) evaluate("window.ZHIXU.importBackup(" + JSONObject.quote(noteOnly.toString()).replace("\u2028", "\\u2028") + ")");
        require(result.getBoolean("ok"), "Valid backup import failed");
        require(Boolean.TRUE.equals(evaluate("document.querySelector('#note-text').value.includes('SMOKE_NOTE') && !window.__noteExecuted")), "Imported note was not treated as text");
        String before = (String) evaluate("localStorage.getItem('" + RECORD_KEY + "')");
        JSONObject invalid = (JSONObject) evaluate("window.ZHIXU.importBackup('{invalid json')");
        require(!invalid.getBoolean("ok"), "Malformed backup was accepted");
        String after = (String) evaluate("localStorage.getItem('" + RECORD_KEY + "')");
        require(before.equals(after), "Failed import changed saved state");
        JSONObject exported = new JSONObject((String) evaluate("window.ZHIXU.exportBackup()"));
        require(exported.getJSONObject("notes").getString(LESSON).contains(dangerousNote), "Backup text did not round-trip");
    }

    private void relaunch() throws Exception {
        evaluate("document.querySelector('#note-text').value='SMOKE_PERSISTED_NOTE';document.querySelector('#note-text').dispatchEvent(new Event('input',{bubbles:true}));window.ZHIXU.handleBack()");
        require(Boolean.TRUE.equals(evaluate("JSON.parse(localStorage.getItem('" + RECORD_KEY + "')).notes['" + LESSON + "']==='SMOKE_PERSISTED_NOTE'")), "Back action did not flush recent note");
        runOnMainSync(() -> reader.finish());
        waitForIdleSync();
        launchReader();
        waitUntil("window.ZHIXU && window.ZHIXU.all.length===182", "Reader failed to relaunch");
        JSONObject backup = new JSONObject((String) evaluate("window.ZHIXU.exportBackup()"));
        require("SMOKE_PERSISTED_NOTE".equals(backup.getJSONObject("notes").getString(LESSON)), "Saved note lost on relaunch");
    }
}

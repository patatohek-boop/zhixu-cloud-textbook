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
import android.view.MotionEvent;
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
    private static final int TOTAL = 14;
    private static final String READY = "window.ZHIXU && window.TEXTBOOK_VERSION && window.TEXTBOOK_VERSION.version==='1.6.1' && window.ZHIXU.all.length===window.TEXTBOOK_VERSION.lessons && window.ZHIXU.all.length===253";
    private Activity reader;
    private WebView web;
    private int number;
    private int failures;
    private String originalRecord;
    private boolean capturedRecord;
    private String migrationAction;
    private boolean expectRelease;
    private final StringBuilder report = new StringBuilder();

    @Override public void onCreate(Bundle arguments) {
        super.onCreate(arguments);
        migrationAction = arguments == null ? null : arguments.getString("migrationAction");
        expectRelease = arguments != null && "true".equals(arguments.getString("expectRelease"));
        start();
    }

    @Override public void onStart() {
        super.onStart();
        if (migrationAction != null) { migration(); return; }
        try {
            launchReader();
            waitUntil(READY, "Revised textbook did not become ready");
            Object original = evaluate("localStorage.getItem('" + RECORD_KEY + "')");
            originalRecord = original instanceof String ? (String) original : null;
            capturedRecord = true;
            runCase("noDangerousPermissions", this::permissions);
            runCase("localOriginOnly", this::origins);
            runCase("readerAndFormulas", this::formulas);
            runCase("revisionAndNavigation", this::revision);
            runCase("conceptNavigationAndMobileLayout", this::concepts);
            runCase("researchRouteAndOfflineLabs", this::researchLabs);
            runCase("simulationAndOfflineLabs", this::simulationLabs);
            runCase("knowledgeFrameworkAndFoundationLabs", this::learningFramework);
            runCase("conceptStoriesOffline", this::conceptStories);
            runCase("tieredPracticeOffline", this::masteryPractice);
            runCase("reportRevisionOffline", this::reportRevision);
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


    /** Synthetic-only migration probe for the isolated CI emulator; never use on personal data. */
    private void migration() {
        Bundle result = new Bundle();
        try {
            launchReader();
            waitUntil(READY, "Migration reader not ready offline");
            waitForReaderFocus();
            String pkg = getTargetContext().getPackageName();
            boolean independent = pkg.equals("app.zhixu.textbook.independent");
            File exported = new File(getTargetContext().getFilesDir(), "migration-export.json");
            if ("seed".equals(migrationAction)) {
                require(!independent, "Seed must run in legacy sandbox");
                require(Boolean.TRUE.equals(evaluate("Object.keys(window.ZHIXU.state.notes).length===0 && window.ZHIXU.state.completed.length===0")), "Seed requires clean synthetic emulator data");
                JSONObject synthetic = new JSONObject();
                synthetic.put("format", "zhixu-learning").put("version", 1);
                synthetic.put("completed", new org.json.JSONArray().put(LESSON));
                synthetic.put("bookmarks", new org.json.JSONArray().put("calculus-04"));
                synthetic.put("notes", new JSONObject().put(LESSON, "MIGRATION_SOURCE_NOTE 合成记录 <script>不会执行</script>"));
                synthetic.put("answers", new JSONObject().put(LESSON, new JSONObject().put("choice", 0).put("at", "2026-10-03T00:00:00Z")));
                JSONObject imported = (JSONObject) evaluate("window.ZHIXU.importBackup(" + JSONObject.quote(synthetic.toString()) + ")");
                require(imported.getBoolean("ok"), "Synthetic seed import failed");
                writeSynthetic(exported, (String) evaluate("window.ZHIXU.exportBackup()"));
            } else if ("empty".equals(migrationAction)) {
                require(independent, "Empty check requires independent sandbox");
                require(Boolean.TRUE.equals(evaluate("Object.keys(window.ZHIXU.state.notes).length===0 && window.ZHIXU.state.completed.length===0 && window.ZHIXU.state.bookmarks.length===0 && Object.keys(window.ZHIXU.state.answers).length===0")), "Independent app read legacy records before explicit import");
            } else if ("import".equals(migrationAction)) {
                require(independent, "Import requires independent sandbox");
                String backup = new String(java.nio.file.Files.readAllBytes(new File(getTargetContext().getFilesDir(), "migration-input.json").toPath()), java.nio.charset.StandardCharsets.UTF_8);
                JSONObject imported = (JSONObject) evaluate("window.ZHIXU.importBackup(" + JSONObject.quote(backup) + ")");
                require(imported.getBoolean("ok"), "Cross-package JSON import failed");
                assertMigrated(false);
                evaluate("window.ZHIXU.state.notes['" + LESSON + "'] += '\\nINDEPENDENT_ONLY';window.ZHIXU.flush()");
                writeSynthetic(exported, (String) evaluate("window.ZHIXU.exportBackup()"));
            } else if ("source".equals(migrationAction)) {
                require(!independent, "Source check requires legacy sandbox");
                assertMigrated(false);
                require(Boolean.TRUE.equals(evaluate("!window.ZHIXU.state.notes['" + LESSON + "'].includes('INDEPENDENT_ONLY')")), "Independent edit changed legacy record");
            } else if ("destination".equals(migrationAction)) {
                require(independent, "Destination check requires independent sandbox");
                assertMigrated(true);
            } else throw new AssertionError("Unknown migration action");
            // Instrumentation.finish terminates its target process immediately. Let WebView's
            // asynchronous localStorage backend commit synthetic writes before that forced exit.
            if ("seed".equals(migrationAction) || "import".equals(migrationAction)) SystemClock.sleep(6000);
            String evidence = (String) evaluate("window.ZHIXU.exportBackup()");
            writeSynthetic(new File(getTargetContext().getFilesDir(), "migration-" + migrationAction + ".json"), evidence);
            result.putString("stream", "\nZHIXU_MIGRATION_SUCCESS " + migrationAction + " " + pkg + "\n");
            if (reader != null) runOnMainSync(() -> reader.finish());
            waitForIdleSync();
            SystemClock.sleep(1000);
            finish(Activity.RESULT_OK, result);
        } catch (Throwable failure) {
            String evidence = "unavailable";
            try { evidence = String.valueOf(evaluate("window.ZHIXU.exportBackup()")); } catch (Throwable ignored) {}
            result.putString("stream", "\nZHIXU_MIGRATION_FAILED " + migrationAction + ": " + failure + "\nSynthetic state: " + evidence + "\n");
            if (reader != null) runOnMainSync(() -> reader.finish());
            finish(Activity.RESULT_CANCELED, result);
        }
    }

    private void writeSynthetic(File file, String text) throws Exception {
        try (FileOutputStream out = new FileOutputStream(file)) {
            out.write(text.getBytes(java.nio.charset.StandardCharsets.UTF_8));
        }
    }

    private void assertMigrated(boolean modified) throws Exception {
        require(Boolean.TRUE.equals(evaluate("window.ZHIXU.state.completed.includes('" + LESSON + "') && window.ZHIXU.state.bookmarks.includes('calculus-04') && window.ZHIXU.state.notes['" + LESSON + "'].includes('MIGRATION_SOURCE_NOTE') && window.ZHIXU.state.answers['" + LESSON + "'].choice===0")), "Progress, bookmark, note, or quiz answer missing after migration/relaunch");
        if (modified) require(Boolean.TRUE.equals(evaluate("window.ZHIXU.state.notes['" + LESSON + "'].includes('INDEPENDENT_ONLY')")), "Independent edit did not persist across relaunch");
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
            waitForReaderFocus();
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

    private void waitForReaderFocus() {
        long until = SystemClock.uptimeMillis() + 10_000;
        boolean[] focused = new boolean[1];
        while (SystemClock.uptimeMillis() < until) {
            runOnMainSync(() -> focused[0] = reader != null && reader.hasWindowFocus());
            if (focused[0]) return;
            SystemClock.sleep(100);
        }
        throw new AssertionError("Emulator window precondition: target reader is not foreground; check system ANR/overlay diagnostics");
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
        require("1.6.1".equals(info.versionName) && info.versionCode == 10, "App version does not match the textbook revision");
        String[] requested = info.requestedPermissions == null ? new String[0] : info.requestedPermissions;
        require(requested.length == 0, "Application must request zero permissions");
        if (expectRelease) require((info.applicationInfo.flags & android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) == 0, "Expected non-debug release app");
        require((BuildConfig.INDEPENDENT ? "app.zhixu.textbook.independent" : "app.zhixu.textbook").equals(info.packageName), "Unexpected distribution identity");
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
        saveReaderScreenshot("reader-screen.png");
    }

    private void saveReaderScreenshot(String filename) throws Exception {
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
        File destination = new File(getTargetContext().getFilesDir(), filename);
        try (FileOutputStream output = new FileOutputStream(destination)) {
            require(screenshot.compress(Bitmap.CompressFormat.PNG, 100, output), "Reader screenshot encoding failed");
            output.flush();
        } finally {
            screenshot.recycle();
        }
    }

    private void simulationLabs() throws Exception {
        evaluate("location.hash='#/simulation'");
        waitUntil("document.querySelectorAll('.simulation-stage').length===6", "Simulation route failed offline");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.simulation-stage .research-lessons a').length===24 && window.COURSES.find(c=>c.id==='fluid-mechanics').chapters.length===62")), "CFD lessons missing");
        for (String lab : new String[]{"cfd-upwind", "cfd-yplus", "cfd-grid", "cfd-cht"}) {
            evaluate("location.hash='#/labs/" + lab + "'");
            waitUntil("document.querySelector('.lab-result') && document.querySelector('.lab-chart svg')", "CFD lab missing");
            Object before = evaluate("document.querySelector('.lab-result').textContent");
            evaluate("(function(){var e=document.querySelector('[data-param]');e.value=e.max;e.dispatchEvent(new Event('input',{bubbles:true}));})()");
            require(!before.equals(evaluate("document.querySelector('.lab-result').textContent")), "CFD control does not update");
            require(Boolean.TRUE.equals(evaluate("!/NaN|Infinity|undefined/.test(document.querySelector('.lab-result').textContent) && document.documentElement.scrollWidth<=innerWidth+1")), "CFD output or layout invalid");
            if ("cfd-cht".equals(lab)) saveReaderScreenshot("simulation-screen.png");
        }
        evaluate("location.hash='#/course/fluid-mechanics/fluid-mechanics-57'");
        waitUntil("document.querySelector('#lesson-body') && document.querySelector('#lesson-body').textContent.includes('48/11')", "Pipe derivation missing");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0 && document.querySelectorAll('#lesson-body .katex').length>20")), "CFD formula rendering failed");
    }

    private void researchLabs() throws Exception {
        evaluate("location.hash='#/research'");
        waitUntil("document.querySelectorAll('.research-stage').length===6", "Research route failed offline");
        require(Boolean.TRUE.equals(evaluate("Array.from(document.querySelectorAll('.research-lessons a')).every(function(a){var id=a.getAttribute('href').split('/').pop();return window.ZHIXU.all.some(function(l){return l.id===id})})")), "Research prerequisite link is broken");
        require(Boolean.TRUE.equals(evaluate("window.COURSES.find(function(c){return c.id==='machine-learning'}).chapters.length===47")), "Research lessons missing from APK");
        require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")), "Research route overflows the phone viewport");
        for (String lab : new String[]{"heat-modes", "cooling-inverse", "experiment-design", "uncertainty-band", "physics-residual", "data-split"}) {
            evaluate("location.hash='#/labs/" + lab + "'");
            waitUntil("document.querySelector('[data-lab=" + lab + "] .lab-chart svg') && document.querySelector('.lab-result').textContent.length>10", "Offline lab missing: " + lab);
            String before = (String) evaluate("document.querySelector('.lab-result').textContent");
            evaluate("(function(){var input=document.querySelector('[data-param]');input.value=input.value===input.max?input.min:input.max;input.dispatchEvent(new Event('input',{bubbles:true}));return true})()");
            String after = (String) evaluate("document.querySelector('.lab-result').textContent");
            require(!before.equals(after), "Lab numerical output did not react: " + lab);
            require(Boolean.TRUE.equals(evaluate("!(/NaN|Infinity/.test(document.querySelector('.lab-chart').innerHTML+document.querySelector('.lab-result').textContent))")), "Invalid graph numbers: " + lab);
            require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")), "Lab overflows the phone viewport: " + lab);
            evaluate("document.querySelector('.lab-reset').click()");
            require(Boolean.TRUE.equals(evaluate("Array.from(document.querySelectorAll('[data-param]')).every(function(input){return Number(input.value)===Number(input.defaultValue)})")), "Lab reset failed: " + lab);
            if ("heat-modes".equals(lab)) saveReaderScreenshot("research-screen.png");
        }
        evaluate("location.hash='#/course/machine-learning/machine-learning-42'");
        // Check the selected lesson against its current content metadata, including every displayed formula.
        waitUntil("window.ZHIXU.state.last==='machine-learning-42' && document.querySelector('#lesson-body h3')"
            + " && document.querySelector('#main h1').textContent===window.ZHIXU.all.find(function(l){return l.id==='machine-learning-42'}).title"
            + " && document.querySelectorAll('#lesson-body .katex-display').length===(window.ZHIXU.all.find(function(l){return l.id==='machine-learning-42'}).content.match(/\\$\\$[\\s\\S]+?\\$\\$/g)||[]).length && document.querySelectorAll('#lesson-body .katex-display').length>4", "PINN lesson did not render offline");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0")), "PINN formulas failed offline");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text')", "Could not return from research labs");
    }

    private void learningFramework() throws Exception {
        require(Boolean.TRUE.equals(evaluate("window.LEARNING_GUIDES.length===30 && !!window.KnowledgeMap && !!window.TextbookNav")), "Learning framework assets missing offline");
        evaluate("location.hash='#/map'");
        waitUntil("document.querySelectorAll('.subject-links a').length===7 && document.querySelector('#relation-select')", "Seven-course framework failed offline");
        String[] courseIds = {"calculus", "linear-algebra", "thermodynamics", "heat-transfer", "fluid-mechanics", "python", "machine-learning"};
        for (String course : courseIds) {
            evaluate("location.hash='#/map/" + course + "'");
            waitUntil("document.querySelector('.subject-links a[aria-current=\"page\"]').getAttribute('href')==='#/map/" + course + "' && document.querySelectorAll('#relation-select option').length===window.COURSES.find(function(c){return c.id==='" + course + "'}).chapters.length", "Incomplete offline map: " + course);
            require(Boolean.TRUE.equals(evaluate("Array.from(document.querySelectorAll('#relation-select option')).every(function(o){return window.COURSES.find(function(c){return c.id==='" + course + "'}).chapters.some(function(l){return l.id===o.value})})")), "Unknown lesson in relationship selector: " + course);
            require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=innerWidth+1")), "Course map overflows mobile viewport: " + course);
        }
        evaluate("location.hash='#/map/calculus/calculus-03'");
        waitUntil("document.querySelector('.dependency-current') && document.querySelector('.dependency-current').textContent.includes('导数')", "Local dependency graph missing");
        saveReaderScreenshot("knowledge-map-screen.png");
        evaluate("document.querySelector('#relation-select').value='calculus-04';document.querySelector('#relation-select').dispatchEvent(new Event('change',{bubbles:true}))");
        waitUntil("location.hash==='#/map/calculus/calculus-04' && document.querySelector('#relation-select').value==='calculus-04' && document.querySelector('.dependency-current h2').textContent===window.ZHIXU.all.find(function(l){return l.id==='calculus-04'}).title", "Relationship lesson picker did not change the displayed knowledge point");
        evaluate("location.hash='#/path'");
        waitUntil("document.querySelectorAll('.tree-course').length===7 && document.querySelectorAll('.tree-chapter a').length===253", "Legacy path did not open the complete knowledge tree");
        require(Boolean.TRUE.equals(evaluate("(function(){var chapter=document.querySelector('.tree-course .tree-chapter');if(chapter.open)return false;chapter.querySelector('summary').click();return chapter.open&&chapter.querySelector('a').getBoundingClientRect().height>0})()")), "Knowledge tree chapter did not reveal its lesson links");
        evaluate("location.hash='#/path/calculus'");
        waitUntil("document.querySelectorAll('.course-contents .tree-chapter a').length===window.COURSES.find(function(c){return c.id==='calculus'}).chapters.length", "Legacy course path did not open the complete course contents");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelectorAll('#lesson-body > h2').length>3 && document.querySelector('#mobile-toc-list')", "Continuous lesson and contents missing");
        require(Boolean.TRUE.equals(evaluate("!document.querySelector('#reading-depth,details.advanced-reading,.reader-preflight') && Array.from(document.querySelectorAll('#lesson-body > h2')).every(function(h){return h.getBoundingClientRect().height>0})")), "Formal explanation is still hidden behind an outer reading layer");
        evaluate("window.__proofHeading=Array.from(document.querySelectorAll('#lesson-body > h2')).find(function(h){return /证明|推导|可导等价/.test(h.textContent)});if(window.__proofHeading)document.querySelector('[data-scroll=\"'+window.__proofHeading.id+'\"]').click()");
        waitUntil("window.__proofHeading && document.activeElement===window.__proofHeading && !window.__proofHeading.closest('details')", "TOC did not focus the continuously visible derivation");
        evaluate("document.querySelector('#lesson-body figure a').click()");
        waitUntil("window.FigureViewer.isOpen() && document.querySelector('.figure-enlarged').complete", "Offline diagram enlargement failed");
        require(Boolean.TRUE.equals(evaluate("document.querySelector('.figure-enlarged').naturalWidth>0")), "Offline enlarged diagram failed to load");
        require(Boolean.TRUE.equals(evaluate("window.ZHIXU.handleBack() && !window.FigureViewer.isOpen() && location.hash==='#/course/calculus/calculus-03'")), "Android back did not close the enlarged figure in place");
        for (String lab : new String[]{"foundation-energy", "foundation-projection", "foundation-mass"}) {
            evaluate("location.hash='#/labs/" + lab + "'");
            waitUntil("document.querySelector('[data-lab=\"" + lab + "\"] .lab-chart svg')", "Foundation lab unavailable offline: " + lab);
            require(Boolean.TRUE.equals(evaluate("(function(){var el=document.querySelector('[data-param]'),before=document.querySelector('.lab-result').textContent;el.value=Number(el.value)===Number(el.max)?el.min:el.max;el.dispatchEvent(new Event('input'));return document.querySelector('.lab-result').textContent!==before})()")), "Foundation controls did not update: " + lab);
            require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=innerWidth+1")), "Foundation lab overflows mobile viewport: " + lab);
        }
    }

    private void conceptStories() throws Exception {
        String[] lessons = {"thermodynamics/thermodynamics-05", "heat-transfer/heat-transfer-03", "heat-transfer/heat-transfer-07", "fluid-mechanics/fluid-mechanics-07", "python/python-06", "machine-learning/machine-learning-07"};
        for (String lesson : lessons) {
            evaluate("location.hash='#/course/" + lesson + "'");
            String lessonId = lesson.substring(lesson.indexOf('/') + 1);
            waitUntil("window.ZHIXU.state.last==='" + lessonId + "' && document.querySelector('.article-head h1').textContent===window.ZHIXU.all.find(function(l){return l.id==='" + lessonId + "'}).title && document.querySelector('.concept-story svg') && document.querySelector('[data-story-action=next]')", "Concept story failed offline: " + lesson);
            require(Boolean.TRUE.equals(evaluate("(function(){var el=document.querySelector('.concept-story'),before=el.textContent;el.querySelector('[data-story-action=next]').click();return el.textContent!==before})()")), "Story step did not change the explanation: " + lesson);
            require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=innerWidth+1 && document.querySelectorAll('.math-error').length===0")), "Story layout or formula failed: " + lesson);
            evaluate("document.querySelector('[data-story-action=replay]').click()");
        }
        evaluate("document.querySelector('.concept-story').scrollIntoView({block:'start',behavior:'instant'})");
        saveReaderScreenshot("concept-story-screen.png");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text')", "Could not return from concept stories");
    }

    private void masteryPractice() throws Exception {
        require(Boolean.TRUE.equals(evaluate("window.MASTERY_EXERCISES.length>=78 && window.TEXTBOOK_VERSION.mastery_lessons===26")), "Mastery exercises missing offline");
        String[] lessons = {"calculus/calculus-03", "fluid-mechanics/fluid-mechanics-01", "python/python-07", "machine-learning/machine-learning-07"};
        for (String lesson : lessons) {
            String lessonId = lesson.substring(lesson.indexOf('/') + 1);
            evaluate("location.hash='#/course/" + lesson + "'");
            waitUntil("window.ZHIXU.state.last==='" + lessonId + "' && document.querySelectorAll('.mastery-card').length===3", "Mastery lesson failed offline: " + lesson);
            require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.mastery-answer[open]').length===0 && document.querySelector('.mastery-intro').textContent.includes('不会自动评分')")), "Practice must begin without revealed answers or false grading claims");
            evaluate("document.querySelector('.mastery-answer summary').click()");
            require(Boolean.TRUE.equals(evaluate("document.querySelector('.mastery-answer').open && document.querySelectorAll('.mastery-checkpoints li').length>=6")), "Practice solution or self-check missing");
            evaluate("document.querySelector('.mastery-answer summary').click()");
            require(Boolean.TRUE.equals(evaluate("!document.querySelector('.mastery-answer').open")), "Repeated disclosure failed");
            evaluate("document.querySelectorAll('.mastery-answer').forEach(function(e){e.open=true})");
            require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0 && document.documentElement.scrollWidth<=innerWidth+1 && document.querySelectorAll('.mastery-card [data-answer],.mastery-card input').length===0")), "Practice formulas, mobile layout or grading contract failed");
            if ("fluid-mechanics-01".equals(lessonId)) formulaTouchScroll();
        }
        evaluate("document.querySelector('.mastery-card').scrollIntoView({block:'start',behavior:'instant'})");
        saveReaderScreenshot("mastery-practice-screen.png");
    }

    private void reportRevision() throws Exception {
        evaluate("location.hash='#/path'");
        waitUntil("document.querySelectorAll('.tree-course').length===7 && document.querySelectorAll('.tree-chapter a').length===253", "Revised complete knowledge tree missing offline");
        require(Boolean.TRUE.equals(evaluate("Array.from(document.querySelectorAll('.tree-chapter a')).every(function(a){return window.ZHIXU.all.some(function(l){return a.getAttribute('href')==='#/course/'+l.course.id+'/'+l.id})}) && document.querySelectorAll('.tree-supplement a').length===2 && document.documentElement.scrollWidth<=innerWidth+1")), "Knowledge tree lesson links, subject indices or mobile layout invalid");
        evaluate("document.querySelector('.tree-course h2').scrollIntoView({block:'start',behavior:'instant'})");
        saveReaderScreenshot("knowledge-tree-screen.png");
        String[] lessons = {"calculus/calculus-02", "calculus/calculus-04", "linear-algebra/linear-algebra-05", "linear-algebra/linear-algebra-06", "thermodynamics/thermodynamics-04", "heat-transfer/heat-transfer-30", "machine-learning/machine-learning-03", "machine-learning/machine-learning-06", "fluid-mechanics/fluid-mechanics-39"};
        for (String lesson : lessons) {
            String id = lesson.substring(lesson.indexOf('/') + 1);
            evaluate("location.hash='#/course/" + lesson + "'");
            waitUntil("window.ZHIXU.state.last==='"+id+"' && document.querySelector('#lesson-body')", "Revised lesson missing offline: "+lesson);
            evaluate("document.querySelectorAll('#lesson-body details').forEach(function(d){d.open=true})");
            require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0 && document.documentElement.scrollWidth<=innerWidth+1")), "Revised lesson fails formula/layout check: "+lesson);
            require(Boolean.TRUE.equals(evaluate("Array.from(document.querySelectorAll('#lesson-body figure img')).every(function(img){return img.getAttribute('src').indexOf('assets/')===0})")), "Revised lesson uses a remote figure: "+lesson);
            if ("fluid-mechanics-39".equals(id)) {
                evaluate("Array.from(document.querySelectorAll('#lesson-body h3')).find(function(h){return h.textContent.includes('绝热液体')}).scrollIntoView({block:'start',behavior:'instant'})");
                saveReaderScreenshot("report-revision-screen.png");
            }
        }
    }

    private void formulaTouchScroll() throws Exception {
        require(Boolean.TRUE.equals(evaluate("(function(){var e=Array.from(document.querySelectorAll('.mastery-card .katex-display')).find(function(x){return x.scrollWidth>x.clientWidth+4});if(!e)return false;e.id='native-scroll-formula';e.scrollIntoView({block:'center',behavior:'instant'});return true})()")), "No overflowing formula available for native touch check");
        waitUntil("(function(){var r=document.querySelector('#native-scroll-formula').getBoundingClientRect();return r.top>0&&r.bottom<innerHeight})()", "Touch formula is not visible");
        for (int i=0; i<4; i++) {
            swipeFormula(true);
            if (Boolean.TRUE.equals(evaluate("(function(){var e=document.querySelector('#native-scroll-formula');return e.scrollWidth-e.clientWidth-e.scrollLeft<=1})()"))) break;
        }
        waitUntil("(function(){var e=document.querySelector('#native-scroll-formula'),r=e.getBoundingClientRect();return e.scrollLeft>0&&e.scrollWidth-e.clientWidth-e.scrollLeft<=1&&e.firstElementChild.getBoundingClientRect().right<=r.right+1})()", "Native touch cannot reveal formula's rightmost symbols");
        saveReaderScreenshot("horizontal-formula-screen.png");
        for (int i=0; i<4; i++) {
            swipeFormula(false);
            if (Boolean.TRUE.equals(evaluate("document.querySelector('#native-scroll-formula').scrollLeft<=1"))) break;
        }
        waitUntil("document.querySelector('#native-scroll-formula').scrollLeft<=1", "Native touch cannot return to formula's left edge");
    }

    private void swipeFormula(boolean towardsRightEdge) throws Exception {
        waitForReaderFocus();
        JSONObject box = (JSONObject) evaluate("(function(){var e=document.querySelector('#native-scroll-formula'),r=e.getBoundingClientRect();return {left:r.left,right:r.right,y:r.top+r.height/2,viewport:innerWidth}})()");
        int[] location = new int[2]; int[] width = new int[1];
        runOnMainSync(() -> { web.getLocationOnScreen(location); width[0]=web.getWidth(); });
        double scale = width[0] / box.getDouble("viewport");
        float left = (float)(location[0]+(box.getDouble("left")+12)*scale);
        float right = (float)(location[0]+(box.getDouble("right")-12)*scale);
        float y = (float)(location[1]+box.getDouble("y")*scale);
        float start = towardsRightEdge ? right : left, end = towardsRightEdge ? left : right;
        long down = SystemClock.uptimeMillis();
        MotionEvent event = MotionEvent.obtain(down, down, MotionEvent.ACTION_DOWN, start, y, 0);
        sendPointerSync(event); event.recycle();
        for (int i=1; i<=12; i++) {
            SystemClock.sleep(16);
            event = MotionEvent.obtain(down, SystemClock.uptimeMillis(), MotionEvent.ACTION_MOVE, start+(end-start)*i/12f, y, 0);
            sendPointerSync(event); event.recycle();
        }
        event = MotionEvent.obtain(down, SystemClock.uptimeMillis(), MotionEvent.ACTION_UP, end, y, 0);
        sendPointerSync(event); event.recycle();
        SystemClock.sleep(250);
    }

    private void invalidRoute() throws Exception {
        evaluate("window.__smokeError=0;window.addEventListener('error',function(){window.__smokeError++});location.hash='#/labs/__proto__'");
        waitUntil("document.querySelector('.labs-index')", "Invalid laboratory route broke the page");
        require(Boolean.TRUE.equals(evaluate("window.__smokeError===0")), "Invalid route raised an error");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text')", "Could not return to lesson");
    }

    private void concepts() throws Exception {
        evaluate("location.hash='#/course/fluid-mechanics/fluid-mechanics-04'");
        waitUntil("document.querySelector('#lesson-body h3') && document.querySelector('#lesson-body').textContent.includes('四分之一圆柱闸门')", "Segmented fluid lesson did not render");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('#mobile-toc-list .toc-concept').length===document.querySelectorAll('#lesson-body h3').length")), "Concepts are missing from mobile navigation");
        waitForConceptLayout();
        tapVisible("#menu", false);
        waitUntil("document.querySelector('#course-sidebar').classList.contains('open') && document.querySelector('#menu').getAttribute('aria-expanded')==='true'", "Mobile course tree did not open");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.sidebar-tree .tree-chapter a').length===window.COURSES.find(function(c){return c.id==='fluid-mechanics'}).chapters.length")), "Mobile course tree omits lessons");
        tapVisible("[data-close-sidebar]", false);
        waitUntil("!document.querySelector('#course-sidebar').classList.contains('open') && document.querySelector('#menu').getAttribute('aria-expanded')==='false'", "Mobile course tree close control failed");
        require(Boolean.TRUE.equals(evaluate("!document.querySelector('.reader-preflight') && !document.querySelector('.reading-tools').open && !document.querySelector('#my-notes').open")), "Reading tools or notes should begin collapsed without a preflight layer");
        tapVisible(".reading-tools > summary", false);
        waitUntil("document.querySelector('.reading-tools').open", "Reading tools did not open after native tap");
        Object wasBookmarked = evaluate("document.querySelector('#bookmark').getAttribute('aria-pressed')");
        tapVisible(".reading-tools #bookmark", false);
        require(!wasBookmarked.equals(evaluate("document.querySelector('#bookmark').getAttribute('aria-pressed')")), "Bookmark did not update inside reading tools");
        tapVisible(".reading-tools #bookmark", false);
        require(wasBookmarked.equals(evaluate("document.querySelector('#bookmark').getAttribute('aria-pressed')")), "Bookmark did not restore after second tap");
        tapVisible(".reading-tools > summary", false);
        tapVisible("#my-notes > summary", false);
        waitUntil("document.querySelector('#my-notes').open && document.querySelector('#note-text').getBoundingClientRect().height>0", "Notes did not become visible after native tap");
        tapVisible("#my-notes > summary", false);
        tapVisible(".mobile-toc > summary", false);
        waitUntil("document.querySelector('.mobile-toc').open", "Concept outline did not open after native tap");
        tapVisible("#mobile-toc-list .toc-concept", true);
        waitForConceptPosition();
        require(Boolean.TRUE.equals(evaluate("location.hash==='#/course/fluid-mechanics/fluid-mechanics-04'")), "Concept navigation left the chapter");
        require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")), "Lesson overflows the mobile viewport horizontally");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0")), "New fluid formulas failed to render");
        saveReaderScreenshot("concept-screen.png");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text') && document.querySelector('#lesson-body').textContent.includes('导数')", "Could not return from concept test");
    }

    private void waitForConceptLayout() throws Exception {
        evaluate("window.__conceptLayoutReady=false;document.fonts.ready.then(function(){requestAnimationFrame(function(){requestAnimationFrame(function(){window.__conceptLayoutReady=true})})})");
        waitUntil("window.__conceptLayoutReady", "Concept fonts and layout did not become ready");
        CountDownLatch ready = new CountDownLatch(1);
        runOnMainSync(() -> web.postVisualStateCallback(SystemClock.uptimeMillis(), new WebView.VisualStateCallback() {
            @Override public void onComplete(long requestId) { ready.countDown(); }
        }));
        require(ready.await(15, TimeUnit.SECONDS), "Concept visual frame did not become ready");
    }

    private void tapVisible(String selector, boolean captureOutline) throws Exception {
        waitForReaderFocus();
        String selected = "document.querySelector(" + JSONObject.quote(selector) + ")";
        evaluate(selected + ".scrollIntoView({block:'center',behavior:'instant'})");
        waitForConceptLayout();
        waitUntil("(function(){var e=" + selected + ",r=e.getBoundingClientRect(),bar=document.querySelector('.topbar').getBoundingClientRect();var hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return r.width>0&&r.height>0&&r.top>=bar.bottom&&r.bottom<=innerHeight&&(hit===e||e.contains(hit))})()", "Concept control is not visibly tappable: " + selector);
        if (captureOutline) saveReaderScreenshot("concept-toc-screen.png");
        JSONObject box = (JSONObject) evaluate("(function(){var r=" + selected + ".getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height/2,viewport:innerWidth}})()");
        int[] location = new int[2]; int[] width = new int[1];
        runOnMainSync(() -> { web.getLocationOnScreen(location); width[0]=web.getWidth(); });
        double scale = width[0] / box.getDouble("viewport");
        float x = (float)(location[0] + box.getDouble("x") * scale);
        float y = (float)(location[1] + box.getDouble("y") * scale);
        long down = SystemClock.uptimeMillis();
        MotionEvent event = MotionEvent.obtain(down, down, MotionEvent.ACTION_DOWN, x, y, 0);
        sendPointerSync(event); event.recycle();
        SystemClock.sleep(80);
        event = MotionEvent.obtain(down, SystemClock.uptimeMillis(), MotionEvent.ACTION_UP, x, y, 0);
        sendPointerSync(event); event.recycle();
    }

    private void waitForConceptPosition() throws Exception {
        long until = SystemClock.uptimeMillis() + 30_000;
        double previousTop = Double.NaN;
        double previousScroll = Double.NaN;
        int stableIntervals = 0;
        int observations = 0;
        JSONObject lastPosition = null;
        while (SystemClock.uptimeMillis() < until) {
            JSONObject position = (JSONObject) evaluate("(function(){"
                + "var heading=document.querySelector('#lesson-body h3'),toolbar=document.querySelector('.topbar');"
                + "var rect=heading.getBoundingClientRect(),toolbarBottom=toolbar.getBoundingClientRect().bottom;"
                + "var padding=parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0;"
                + "var margin=parseFloat(getComputedStyle(heading).scrollMarginTop)||0;"
                + "return {top:rect.top,bottom:rect.bottom,scroll:window.scrollY,toolbarBottom:toolbarBottom,padding:padding,margin:margin,innerHeight:innerHeight,fonts:document.fonts.status,tocOpen:document.querySelector('.mobile-toc').open,focused:document.activeElement===heading,visible:rect.height>0&&rect.top>=toolbarBottom"
                + "&&rect.bottom<=window.innerHeight&&Math.abs(rect.top-(padding+margin))<=1};})()");
            lastPosition = position;
            if (observations++ % 20 == 0) report.append("CONCEPT_POSITION ").append(position.toString()).append('\n');
            double top = position.getDouble("top");
            double scroll = position.getDouble("scroll");
            // Coordinates and rounding tolerance are CSS pixels, independent of screen density.
            // Require two stable polling intervals at the expected alignment before the screenshot.
            if (position.getBoolean("visible") && Math.abs(top - previousTop) <= 0.5
                    && Math.abs(scroll - previousScroll) <= 0.5) {
                if (++stableIntervals >= 2) {
                    report.append("CONCEPT_POSITION_SETTLED ").append(position.toString()).append('\n');
                    return;
                }
            } else {
                stableIntervals = 0;
            }
            previousTop = top;
            previousScroll = scroll;
            SystemClock.sleep(150);
        }
        try { saveReaderScreenshot("concept-position-failure-screen.png"); }
        catch (Throwable captureFailure) { report.append("CONCEPT_CAPTURE ").append(captureFailure.toString()).append('\n'); }
        throw new AssertionError("Concept heading did not settle visibly below the toolbar: " + lastPosition);
    }

    private void revision() throws Exception {
        require(Boolean.TRUE.equals(evaluate("window.TEXTBOOK_VERSION.reviewed===window.ZHIXU.all.length && window.CONTENT_REVIEW.length===7")), "Incomplete chapter audit payload");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('#mobile-toc-list [data-scroll]').length>3 && !!document.querySelector('.prereq a')")), "Mobile reading navigation missing");
        evaluate("location.hash='#/review/fluid-mechanics/fluid-mechanics-30'");
        waitUntil("document.querySelector('#review-fluid-mechanics-30[open]')", "Chapter revision deep link failed");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.review-record').length===window.COURSES.filter(function(c){return c.id==='fluid-mechanics'})[0].chapters.length && document.querySelectorAll('.review-map a').length>30")), "Coverage map is incomplete");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text')", "Could not return from revision to lesson");
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
        waitUntil(READY, "Reader failed to relaunch");
        JSONObject backup = new JSONObject((String) evaluate("window.ZHIXU.exportBackup()"));
        require("SMOKE_PERSISTED_NOTE".equals(backup.getJSONObject("notes").getString(LESSON)), "Saved note lost on relaunch");
    }
}

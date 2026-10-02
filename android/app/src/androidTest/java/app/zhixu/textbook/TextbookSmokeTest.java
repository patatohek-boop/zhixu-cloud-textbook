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
    private static final int TOTAL = 13;
    private static final String READY = "window.ZHIXU && window.TEXTBOOK_VERSION && window.TEXTBOOK_VERSION.version==='1.4.0' && window.ZHIXU.all.length===window.TEXTBOOK_VERSION.lessons && window.ZHIXU.all.length>182";
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
        require("1.4.0".equals(info.versionName) && info.versionCode == 7, "App version does not match the textbook revision");
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
        // Lesson 42 contains exactly nine displayed formulas; require all of them in the correct lesson.
        waitUntil("window.ZHIXU.state.last==='machine-learning-42' && document.querySelector('#lesson-body h3')"
            + " && document.querySelector('#main h1').textContent==='PINN：把热方程写进学习目标'"
            + " && document.querySelectorAll('#lesson-body .katex').length===9", "PINN lesson did not render offline");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0")), "PINN formulas failed offline");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text')", "Could not return from research labs");
    }

    private void learningFramework() throws Exception {
        require(Boolean.TRUE.equals(evaluate("window.LEARNING_GUIDES.length===26 && !!window.KnowledgeMap")), "Learning framework assets missing offline");
        evaluate("location.hash='#/map'");
        waitUntil("document.querySelectorAll('.map-course-card').length===7", "Seven-course framework failed offline");
        String[] courseIds = {"calculus", "linear-algebra", "thermodynamics", "heat-transfer", "fluid-mechanics", "python", "machine-learning"};
        for (String course : courseIds) {
            evaluate("location.hash='#/map/" + course + "'");
            waitUntil("document.querySelectorAll('[data-node-id]').length===window.COURSES.find(function(c){return c.id==='" + course + "'}).chapters.length", "Incomplete offline map: " + course);
            require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=innerWidth+1")), "Course map overflows mobile viewport: " + course);
        }
        evaluate("location.hash='#/map/calculus/calculus-03'");
        waitUntil("document.querySelector('.dependency-current') && document.querySelector('.dependency-current').textContent.includes('导数')", "Local dependency graph missing");
        saveReaderScreenshot("knowledge-map-screen.png");
        evaluate("location.hash='#/path'");
        waitUntil("document.querySelectorAll('.core-route>li').length===26", "Core path incomplete offline");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#reading-depth') && document.querySelector('details.advanced-reading')", "Progressive reading controls missing");
        require(Boolean.TRUE.equals(evaluate("(function(){var heading=document.querySelector('details.advanced-reading h2');document.querySelector('[data-scroll=\"'+heading.id+'\"]').click();return heading.closest('details').open && document.activeElement===heading})()")), "TOC did not open and focus an original proof");
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
        }
        evaluate("document.querySelector('.mastery-card').scrollIntoView({block:'start',behavior:'instant'})");
        saveReaderScreenshot("mastery-practice-screen.png");
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
        evaluate("document.querySelector('.mobile-toc').open=true");
        evaluate("document.querySelector('#mobile-toc-list .toc-concept').click()");
        waitForConceptPosition();
        require(Boolean.TRUE.equals(evaluate("location.hash==='#/course/fluid-mechanics/fluid-mechanics-04'")), "Concept navigation left the chapter");
        require(Boolean.TRUE.equals(evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")), "Lesson overflows the mobile viewport horizontally");
        require(Boolean.TRUE.equals(evaluate("document.querySelectorAll('.math-error').length===0")), "New fluid formulas failed to render");
        saveReaderScreenshot("concept-screen.png");
        evaluate("location.hash='#/course/calculus/calculus-03'");
        waitUntil("document.querySelector('#note-text') && document.querySelector('#lesson-body').textContent.includes('导数')", "Could not return from concept test");
    }

    private void waitForConceptPosition() throws Exception {
        long until = SystemClock.uptimeMillis() + 30_000;
        double previousTop = Double.NaN;
        double previousScroll = Double.NaN;
        int stableIntervals = 0;
        while (SystemClock.uptimeMillis() < until) {
            JSONObject position = (JSONObject) evaluate("(function(){"
                + "var heading=document.querySelector('#lesson-body h3'),toolbar=document.querySelector('.topbar');"
                + "var rect=heading.getBoundingClientRect(),toolbarBottom=toolbar.getBoundingClientRect().bottom;"
                + "var padding=parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop)||0;"
                + "var margin=parseFloat(getComputedStyle(heading).scrollMarginTop)||0;"
                + "return {top:rect.top,scroll:window.scrollY,visible:rect.height>0&&rect.top>=toolbarBottom"
                + "&&rect.bottom<=window.innerHeight&&Math.abs(rect.top-(padding+margin))<=1};})()");
            double top = position.getDouble("top");
            double scroll = position.getDouble("scroll");
            // Coordinates and rounding tolerance are CSS pixels, independent of screen density.
            // Require two stable polling intervals at the expected alignment before the screenshot.
            if (position.getBoolean("visible") && Math.abs(top - previousTop) <= 0.5
                    && Math.abs(scroll - previousScroll) <= 0.5) {
                if (++stableIntervals >= 2) return;
            } else {
                stableIntervals = 0;
            }
            previousTop = top;
            previousScroll = scroll;
            SystemClock.sleep(150);
        }
        throw new AssertionError("Concept heading did not settle visibly below the toolbar");
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

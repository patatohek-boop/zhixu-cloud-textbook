package app.zhixu.textbook;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.net.http.SslError;
import android.os.Build;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.ParcelFileDescriptor;
import android.print.PageRange;
import android.print.PrintAttributes;
import android.print.PrintDocumentAdapter;
import android.print.PrintManager;
import android.view.Gravity;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.CookieManager;
import android.webkit.GeolocationPermissions;
import android.webkit.PermissionRequest;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.SslErrorHandler;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.PopupMenu;
import android.widget.TextView;
import android.widget.Toast;
import androidx.webkit.WebViewAssetLoader;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.charset.CodingErrorAction;
import java.nio.ByteBuffer;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** Offline-only reader. No JavaScript interface, network permission or storage permission. */
public final class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String ENTRY = "https://" + HOST + "/assets/www/index.html";
    private static final String WEBSITE = "https://patatohek-boop.github.io/zhixu-cloud-textbook/";
    private static final String RELEASES = "https://github.com/patatohek-boop/zhixu-cloud-textbook/releases";
    private static final int IMPORT = 101;
    private static final int EXPORT = 102;
    private static final int MAX_BACKUP_BYTES = 10_000_000;
    private final ExecutorService files = Executors.newSingleThreadExecutor();
    private WebView web;
    private LinearLayout layout;
    private boolean ready;
    private boolean busy;
    private boolean backPending;
    private boolean waitingForScript;
    private boolean engineWarningShown;
    private int pageGeneration;
    private Uri pendingDocument;
    private int pendingRequest;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setBackgroundColor(Color.rgb(246, 248, 246));
        setContentView(layout);
        configureInsets();
        addToolbar();
        if (state != null) {
            String document = state.getString("pending-document");
            if (document != null) pendingDocument = Uri.parse(document);
            pendingRequest = state.getInt("pending-request", 0);
        }
        createReader(state);
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
                android.window.OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::handleBack);
        }
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    @SuppressWarnings("deprecation")
    private void configureInsets() {
        if (Build.VERSION.SDK_INT >= 30) {
            getWindow().setDecorFitsSystemWindows(false);
            layout.setOnApplyWindowInsetsListener((view, insets) -> {
                android.graphics.Insets bounds = insets.getInsets(
                    WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout()
                        | WindowInsets.Type.ime());
                view.setPadding(bounds.left, bounds.top, bounds.right, bounds.bottom);
                return insets;
            });
            WindowInsetsController controller = getWindow().getInsetsController();
            if (controller != null) controller.setSystemBarsAppearance(
                WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
                    | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,
                WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
                    | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS);
        } else {
            getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        }
    }

    private void addToolbar() {
        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        toolbar.setPadding(dp(16), 0, dp(8), 0);
        TextView title = new TextView(this);
        title.setText(R.string.offline_title);
        title.setTextSize(14);
        title.setTextColor(Color.rgb(34, 82, 68));
        toolbar.addView(title, new LinearLayout.LayoutParams(0, dp(44), 1));
        title.setGravity(Gravity.CENTER_VERTICAL);
        Button menu = new Button(this);
        menu.setText(R.string.app_menu);
        menu.setTextSize(13);
        menu.setAllCaps(false);
        menu.setMinHeight(0);
        menu.setMinimumHeight(0);
        menu.setOnClickListener(this::showMenu);
        toolbar.addView(menu, new LinearLayout.LayoutParams(dp(98), dp(44)));
        layout.addView(toolbar, new LinearLayout.LayoutParams(-1, dp(48)));
    }

    private void showMenu(View anchor) {
        PopupMenu popup = new PopupMenu(this, anchor);
        popup.getMenu().add(0, 1, 0, R.string.menu_home);
        popup.getMenu().add(0, 2, 1, R.string.menu_export);
        popup.getMenu().add(0, 3, 2, R.string.menu_import);
        popup.getMenu().add(0, 4, 3, R.string.menu_print);
        popup.getMenu().add(0, 5, 4, R.string.menu_website);
        popup.getMenu().add(0, 6, 5, R.string.menu_updates);
        popup.getMenu().add(0, 7, 6, R.string.menu_about);
        popup.setOnMenuItemClickListener(item -> {
            switch (item.getItemId()) {
                case 1: if (web != null) web.loadUrl(ENTRY + "#/"); break;
                case 2: chooseDocument(EXPORT); break;
                case 3: chooseDocument(IMPORT); break;
                case 4: printLesson(); break;
                case 5: openBrowser(Uri.parse(WEBSITE)); break;
                case 6: openBrowser(Uri.parse(RELEASES)); break;
                case 7:
                    new AlertDialog.Builder(this).setTitle(R.string.app_name)
                        .setMessage(getString(R.string.about_text, BuildConfig.VERSION_NAME))
                        .setPositiveButton(R.string.got_it, null).show();
                    break;
                default: return false;
            }
            return true;
        });
        popup.show();
    }

    @SuppressWarnings("deprecation")
    private void createReader(Bundle state) {
        ready = false;
        backPending = false;
        engineWarningShown = false;
        web = new WebView(this);
        web.setBackgroundColor(Color.rgb(246, 248, 246));
        web.setImportantForAutofill(View.IMPORTANT_FOR_AUTOFILL_NO_EXCLUDE_DESCENDANTS);
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG);
        WebSettings settings = web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setAllowFileAccessFromFileURLs(false);
        settings.setAllowUniversalAccessFromFileURLs(false);
        settings.setBlockNetworkLoads(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setSupportMultipleWindows(false);
        settings.setGeolocationEnabled(false);
        settings.setMediaPlaybackRequiresUserGesture(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSaveFormData(false);
        CookieManager.getInstance().setAcceptCookie(false);
        CookieManager.getInstance().setAcceptThirdPartyCookies(web, false);
        WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
            .setHttpAllowed(false)
            .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this)).build();
        web.setWebViewClient(new ReaderClient(loader));
        web.setWebChromeClient(new WebChromeClient() {
            @Override public void onPermissionRequest(PermissionRequest request) { request.deny(); }
            @Override public void onGeolocationPermissionsShowPrompt(String origin,
                    GeolocationPermissions.Callback callback) {
                callback.invoke(origin, false, false);
            }
        });
        web.setDownloadListener((url, userAgent, disposition, mime, length) ->
            message("请使用“应用菜单 → 导出学习备份”保存 JSON 文件。"));
        layout.addView(web, new LinearLayout.LayoutParams(-1, 0, 1));
        if (state == null || web.restoreState(state) == null || !isLocalAsset(parse(web.getUrl()))) {
            web.loadUrl(ENTRY);
        }
    }

    private static Uri parse(String value) {
        return value == null ? Uri.EMPTY : Uri.parse(value);
    }

    private static boolean isLocalAsset(Uri uri) {
        return "https".equals(uri.getScheme()) && HOST.equals(uri.getHost())
            && uri.getUserInfo() == null && (uri.getPort() == -1 || uri.getPort() == 443)
            && uri.getPath() != null && uri.getPath().startsWith("/assets/www/")
            && !uri.getPath().contains("..") && !uri.getPath().contains("\\");
    }

    private boolean isReader() {
        return ready && isReaderUrl(parse(web == null ? null : web.getUrl()));
    }

    private static boolean isReaderUrl(Uri uri) {
        return isLocalAsset(uri) && "/assets/www/index.html".equals(uri.getPath())
            && uri.getQuery() == null;
    }

    private final class ReaderClient extends WebViewClient {
        private final WebViewAssetLoader loader;
        ReaderClient(WebViewAssetLoader loader) { this.loader = loader; }

        @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            if ("GET".equals(request.getMethod()) && isLocalAsset(request.getUrl())) {
                WebResourceResponse response = loader.shouldInterceptRequest(request.getUrl());
                if (response != null) {
                    Map<String, String> headers = new HashMap<>();
                    if (response.getResponseHeaders() != null) headers.putAll(response.getResponseHeaders());
                    headers.put("X-Content-Type-Options", "nosniff");
                    headers.put("Referrer-Policy", "no-referrer");
                    response.setResponseHeaders(headers);
                    return response;
                }
            }
            return new WebResourceResponse("text/plain", "UTF-8", 403, "Blocked",
                new HashMap<>(), new ByteArrayInputStream(new byte[0]));
        }

        @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            if ("zhixu".equals(uri.getScheme())) {
                boolean knownCommand = "export".equals(uri.getHost()) || "import".equals(uri.getHost())
                    || "print".equals(uri.getHost());
                boolean trustedPage = request.isForMainFrame() && isReader() && knownCommand
                    && uri.getUserInfo() == null && uri.getPort() == -1
                    && (uri.getPath() == null || uri.getPath().isEmpty())
                    && uri.getQuery() == null && uri.getFragment() == null;
                if (trustedPage && !request.hasGesture()) {
                    message("当前系统未识别到点击，请使用顶部“应用菜单”完成导入、导出或打印。");
                } else if (trustedPage) {
                    switch (String.valueOf(uri.getHost())) {
                        case "export": chooseDocument(EXPORT); break;
                        case "import": chooseDocument(IMPORT); break;
                        case "print": printLesson(); break;
                        default: break;
                    }
                }
                return true;
            }
            if (isLocalAsset(uri)) return false;
            if (request.isForMainFrame() && request.hasGesture()) openBrowser(uri);
            return true;
        }

        @Override public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
            ready = false;
            pageGeneration++;
        }

        @Override public void onPageFinished(WebView view, String url) {
            // Detect unsupported JavaScript syntax with an ES5-only probe. A finished HTML load
            // does not imply the textbook scripts ran, especially on old Android 8 WebViews.
            if (view != web || !isReaderUrl(parse(url)) || !isReaderUrl(parse(view.getUrl()))) return;
            final int generation = pageGeneration;
            view.evaluateJavascript("Boolean(window.ZHIXU && typeof window.ZHIXU.exportBackup === 'function' && typeof window.ZHIXU.importBackup === 'function' && typeof window.ZHIXU.flush === 'function' && typeof window.ZHIXU.handleBack === 'function')", result -> {
                if (!alive() || view != web || generation != pageGeneration
                        || !isReaderUrl(parse(view.getUrl()))) return;
                ready = "true".equals(result);
                if (ready) {
                    if (pendingDocument != null) consumeDocument();
                } else if (!engineWarningShown) {
                    engineWarningShown = true;
                    new AlertDialog.Builder(MainActivity.this).setTitle("教材未能加载")
                        .setMessage("当前系统网页组件可能过旧，无法运行教材。请通过手机应用商店更新 Android System WebView（Android 系统 WebView）和 Chrome，然后重新打开本应用。\n\n也可以使用已更新的浏览器打开网页版。若更新组件后仍出现此提示，请重新安装最新版教材。")
                        .setPositiveButton("打开网页版", (dialog, which) -> openBrowser(Uri.parse(WEBSITE)))
                        .setNegativeButton("退出", (dialog, which) -> finish())
                        .setCancelable(false).show();
                }
            });
        }

        @Override public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
            handler.cancel();
        }

        @Override public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
            if (request.isForMainFrame()) message("教材页面暂时未能打开，请从应用菜单返回书架。无需联网。 ");
        }

        @Override public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {
            ready = false;
            backPending = false;
            if (waitingForScript) { waitingForScript = false; busy = false; }
            layout.removeView(view);
            view.destroy();
            web = null;
            new AlertDialog.Builder(MainActivity.this).setTitle("阅读页面已暂停")
                .setMessage("系统回收了阅读页面。已保存的笔记仍保存在本机，可重新打开教材。")
                .setPositiveButton("重新打开", (dialog, which) -> createReader(null))
                .setNegativeButton("退出", (dialog, which) -> finish()).setCancelable(false).show();
            return true;
        }
    }

    private void openBrowser(Uri uri) {
        if (!("https".equals(uri.getScheme()) || "http".equals(uri.getScheme()))
                || uri.getHost() == null || uri.getUserInfo() != null) return;
        try {
            Intent intent = new Intent(Intent.ACTION_VIEW, uri);
            intent.addCategory(Intent.CATEGORY_BROWSABLE);
            startActivity(intent);
        } catch (ActivityNotFoundException | SecurityException exception) {
            message("没有可打开此链接的浏览器，请先安装浏览器。");
        }
    }

    private void chooseDocument(int request) {
        if (!isReader()) { message("请先打开教材书架或课文，再导入、导出学习记录。"); return; }
        if (busy) { message("正在处理学习备份，请稍候。"); return; }
        Intent intent = new Intent(request == IMPORT ? Intent.ACTION_OPEN_DOCUMENT : Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        if (request == IMPORT) {
            // Some document providers label downloaded JSON as plain text or octet-stream.
            // Validate the actual limited-size content instead of trusting MIME or extension.
            intent.setType("*/*");
        } else {
            intent.setType("application/json");
            String date = new SimpleDateFormat("yyyy-MM-dd", Locale.ROOT).format(new Date());
            intent.putExtra(Intent.EXTRA_TITLE, "知序-学习备份-" + date + ".json");
        }
        try {
            busy = true;
            startActivityForResult(intent, request);
        } catch (ActivityNotFoundException | SecurityException exception) {
            busy = false;
            message("系统文件选择器不可用，请安装或启用系统“文件”应用后重试。");
        }
    }

    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request != IMPORT && request != EXPORT) return;
        busy = false;
        if (result != RESULT_OK || data == null || data.getData() == null) return;
        Uri uri = data.getData();
        if (!"content".equals(uri.getScheme())) { message("文件提供程序返回的地址不受支持。"); return; }
        pendingDocument = uri;
        pendingRequest = request;
        if (isReader()) consumeDocument();
        else if (ready) {
            pendingDocument = null;
            message("请返回教材书架后重新导入或导出备份。");
        }
    }

    private void consumeDocument() {
        Uri document = pendingDocument;
        int request = pendingRequest;
        pendingDocument = null;
        pendingRequest = 0;
        if (document == null || busy) return;
        busy = true;
        if (request == EXPORT) exportDocument(document); else importDocument(document);
    }

    private static JSONObject validateBackup(String text) throws JSONException {
        if (text.getBytes(StandardCharsets.UTF_8).length > MAX_BACKUP_BYTES)
            throw new JSONException("备份超过 10 MB");
        JSONTokener parser = new JSONTokener(text);
        Object value = parser.nextValue();
        if (!(value instanceof JSONObject) || parser.nextClean() != 0)
            throw new JSONException("备份必须是完整的 JSON 对象");
        JSONObject object = (JSONObject) value;
        if (!"zhixu-learning".equals(object.optString("format")) || object.optInt("version", 0) != 1
                || !(object.opt("completed") instanceof JSONArray)
                || !(object.opt("bookmarks") instanceof JSONArray)
                || !(object.opt("notes") instanceof JSONObject)
                || (object.has("answers") && !(object.opt("answers") instanceof JSONObject)))
            throw new JSONException("这不是有效的知序学习备份");
        return object;
    }

    private void exportDocument(Uri document) {
        waitingForScript = true;
        web.evaluateJavascript("window.ZHIXU && window.ZHIXU.exportBackup()", encoded -> {
            waitingForScript = false;
            if (!isReader()) { finishFileTask("页面已切换，请重新导出备份。"); return; }
            files.execute(() -> {
                try {
                    Object result = new JSONTokener(encoded).nextValue();
                    if (!(result instanceof String)) throw new JSONException("教材尚未准备好导出");
                    String text = (String) result;
                    validateBackup(text);
                    byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
                    try (OutputStream output = getContentResolver().openOutputStream(document, "wt")) {
                        if (output == null) throw new java.io.IOException("无法写入所选文件");
                        output.write(bytes);
                        output.flush();
                    }
                    finishFileTask("学习备份已保存。请妥善保管，备份包含你的笔记。");
                } catch (Exception exception) {
                    finishFileTask("导出失败：" + safeError(exception) + "。请重新选择保存位置。");
                }
            });
        });
    }

    private void importDocument(Uri document) {
        files.execute(() -> {
            try {
                String text;
                try (InputStream input = getContentResolver().openInputStream(document)) {
                    if (input == null) throw new java.io.IOException("无法读取所选文件");
                    ByteArrayOutputStream bytes = new ByteArrayOutputStream();
                    byte[] buffer = new byte[8192];
                    int count;
                    while ((count = input.read(buffer)) != -1) {
                        if (bytes.size() + count > MAX_BACKUP_BYTES) throw new java.io.IOException("备份超过 10 MB");
                        bytes.write(buffer, 0, count);
                    }
                    text = StandardCharsets.UTF_8.newDecoder()
                        .onMalformedInput(CodingErrorAction.REPORT)
                        .onUnmappableCharacter(CodingErrorAction.REPORT)
                        .decode(ByteBuffer.wrap(bytes.toByteArray())).toString();
                }
                validateBackup(text);
                // JSONObject.quote preserves the file as one JS string argument; file contents never become code.
                String argument = JSONObject.quote(text).replace("\u2028", "\\u2028").replace("\u2029", "\\u2029");
                runOnUiThread(() -> {
                    if (!alive() || !isReader()) {
                        finishFileTask("页面已切换，请重新导入备份；原记录未更改。");
                        return;
                    }
                    waitingForScript = true;
                    web.evaluateJavascript("window.ZHIXU && window.ZHIXU.importBackup(" + argument + ")", result -> {
                        waitingForScript = false;
                        try {
                            JSONObject outcome = new JSONObject(result);
                            if (!Boolean.TRUE.equals(outcome.opt("ok"))) {
                                String reason = outcome.optString("error", "教材尚未准备好导入");
                                finishFileTask("导入失败：" + reason.substring(0, Math.min(reason.length(), 300)));
                                return;
                            }
                            finishFileTask("备份已合并并保存，原有笔记已保留。");
                        } catch (Exception exception) {
                            finishFileTask("导入失败：" + safeError(exception));
                        }
                    });
                });
            } catch (Exception exception) {
                finishFileTask("导入失败：" + safeError(exception) + "；原记录未更改。");
            }
        });
    }

    private static String safeError(Exception exception) {
        if (exception instanceof JSONException) return "备份格式无效或内容不完整";
        if (exception.getMessage() != null && exception.getMessage().contains("10 MB")) return "备份超过 10 MB";
        return "无法完成文件读写，请检查文件是否可用以及存储空间";
    }

    private void finishFileTask(String text) {
        runOnUiThread(() -> { busy = false; if (alive()) message(text); });
    }

    private void printLesson() {
        if (!isReader()) { message("请先打开要打印的课文。"); return; }
        PrintManager manager = (PrintManager) getSystemService(PRINT_SERVICE);
        if (manager == null) { message("此设备暂不支持系统打印。"); return; }
        final WebView printingView = web;
        printingView.evaluateJavascript("window.__zhixuPrintClosed=Array.from(document.querySelectorAll('.prose details:not([open])'));window.__zhixuPrintClosed.forEach(function(item){item.open=true});true", ignored -> {
            if (!alive() || web != printingView || !isReader()) return;
            try {
                PrintDocumentAdapter delegate = printingView.createPrintDocumentAdapter("知序云教材");
                PrintDocumentAdapter adapter = new PrintDocumentAdapter() {
                    @Override public void onStart() { delegate.onStart(); }
                    @Override public void onLayout(PrintAttributes oldAttributes, PrintAttributes newAttributes,
                            CancellationSignal cancellation, LayoutResultCallback callback, Bundle extras) {
                        delegate.onLayout(oldAttributes, newAttributes, cancellation, callback, extras);
                    }
                    @Override public void onWrite(PageRange[] pages, ParcelFileDescriptor destination,
                            CancellationSignal cancellation, WriteResultCallback callback) {
                        delegate.onWrite(pages, destination, cancellation, callback);
                    }
                    @Override public void onFinish() {
                        delegate.onFinish();
                        restorePrintedDetails(printingView);
                    }
                };
                manager.print("知序云教材", adapter, new PrintAttributes.Builder().build());
            } catch (RuntimeException exception) {
                restorePrintedDetails(printingView);
                message("未能打开打印面板，请稍后重试。");
            }
        });
    }

    private void restorePrintedDetails(WebView printingView) {
        if (alive() && web == printingView && isReader())
            printingView.evaluateJavascript("(window.__zhixuPrintClosed||[]).forEach(function(item){item.open=false});delete window.__zhixuPrintClosed", null);
    }

    private void handleBack() {
        if (web == null) { finish(); return; }
        if (backPending) return;
        if (!isReader()) { nativeBack(); return; }
        backPending = true;
        web.evaluateJavascript("Boolean(window.ZHIXU && window.ZHIXU.handleBack())", handled -> {
            backPending = false;
            if (alive() && !"true".equals(handled)) nativeBack();
        });
    }

    private void nativeBack() {
        if (web != null && web.canGoBack()) web.goBack(); else finish();
    }

    @SuppressWarnings("deprecation")
    @Override public void onBackPressed() { handleBack(); }

    private void flushNotes() {
        if (isReader()) web.evaluateJavascript("window.ZHIXU && window.ZHIXU.flush()", null);
    }

    @Override protected void onPause() {
        flushNotes();
        if (web != null) web.onPause();
        super.onPause();
    }

    @Override protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override protected void onSaveInstanceState(Bundle state) {
        flushNotes();
        if (web != null) web.saveState(state);
        if (pendingDocument != null) state.putString("pending-document", pendingDocument.toString());
        state.putInt("pending-request", pendingRequest);
        super.onSaveInstanceState(state);
    }

    @Override protected void onDestroy() {
        if (web != null) {
            layout.removeView(web);
            web.stopLoading();
            web.destroy();
            web = null;
        }
        files.shutdown();
        super.onDestroy();
    }

    private boolean alive() { return !isFinishing() && !isDestroyed(); }
    private void message(String text) { if (alive()) Toast.makeText(this, text, Toast.LENGTH_LONG).show(); }
}

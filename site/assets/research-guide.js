/* A problem-led route through the existing textbook and thermal AI extension. */
(() => {
 'use strict';
 const stages = [
  {title:'先把温度变化讲清楚',question:'温度为什么变化，哪些条件决定唯一的解？',ids:['heat-transfer-02','heat-transfer-07','heat-transfer-08','linear-algebra-13'],lab:'heat-modes',labName:'把温度场拆成逐渐衰减的波',deliverable:'画出物体边界，写明初始温度、边界条件、单位和适用的物性假设。能解释 Bi、Fo，以及何时不能把整个物体当作一个温度。'},
  {title:'让一次实验成为可用的数据',question:'记录的是物体温度，还是传感器的响应？',ids:['python-13','python-20','python-25','machine-learning-36','machine-learning-37'],lab:'data-split',labName:'同一次实验的样本为什么不能随意打散',deliverable:'整理实验批次、试件、工况、采样时间、标定与不确定度；明确哪些数据只用于最终测试。先用合成数据练习，再接入自己的实验。'},
  {title:'从测量反推物理参数',question:'曲线拟合很好，就一定找到了真实换热系数吗？',ids:['linear-algebra-11','linear-algebra-20','machine-learning-31','machine-learning-38','machine-learning-39'],lab:'cooling-inverse',labName:'亲手调整换热系数，比较观测与预测',deliverable:'完成一个带单位的反演例题；说明可辨识性、噪声假设和参数区间，区分测量噪声、物性不确定性与模型误差。'},
  {title:'用小样本安排下一次实验',question:'下一次测哪里，最能减少疑问？',ids:['machine-learning-05','machine-learning-06','machine-learning-35','machine-learning-40','machine-learning-41'],lab:'experiment-design',labName:'不同测量时刻提供多少参数信息',deliverable:'比较物理基线和概率代理；预先写清优化目标或估参目标、实验预算和可行域。保留重复实验与独立核验，不只追逐一个最优预测。'},
  {title:'让模型遵守物理，再检验它',question:'方程残差小，为什么温度场仍可能错误？',ids:['machine-learning-18','machine-learning-19','heat-transfer-10','machine-learning-42','machine-learning-43','machine-learning-44','machine-learning-45'],lab:'physics-residual',labName:'零方程残差也可能不是目标问题的解',deliverable:'对解析制造解核对导数、初边值与误差；比较传统求解器、数据模型和物理约束模型。报告训练成本、守恒误差和分布外失效。'},
  {title:'做完一个能复现的研究闭环',question:'另一位研究者能复算，并指出模型何时失效吗？',ids:['heat-transfer-20','machine-learning-29','machine-learning-26','machine-learning-46','machine-learning-47','python-26'],lab:'uncertainty-band',labName:'区分平均响应区间和新观测的预测区间',deliverable:'提交数据说明、按实验批次划分的清单、基线、消融、误差与区间报告、失败案例和下一次实验方案。保存原始记录及运行环境。'}
 ];
 const escape = value => String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function render(courses, completed=[]) {
  const lessons=new Map(courses.flatMap(c=>c.chapters.map(l=>[l.id,{...l,course:c.id}])));
  const link=id=>{const l=lessons.get(id);return l?`<a href="#/course/${escape(l.course)}/${escape(id)}"><span class="research-check" aria-label="${completed.includes(id)?'已记录完成':'未记录完成'}">${completed.includes(id)?'✓':'○'}</span>${escape(l.title)}</a>`:'';};
  const novel=Array.from({length:12},(_,i)=>'machine-learning-'+(36+i));
  const first=novel.find(id=>!completed.includes(id))||novel[0];
  return `<main class="page research-page" id="main" tabindex="-1">
   <header class="research-hero"><div class="eyebrow">THERMAL SCIENCE · DATA · EXPERIMENT</div><h1>把 AI 用到传热与实验中。</h1><p class="lead">从一个可以测量、可以解释、可以检验的问题出发。先修基础沿途可回看，进阶内容按研究任务串联。</p><div class="button-row"><a class="primary" href="#/course/machine-learning/${first}">开始研究方向课程 →</a><a class="secondary" href="#/course/machine-learning">查看完整机器学习目录</a></div><p class="muted small">机器学习基础 35 节＋研究方向 12 节。进度沿用课文完成记录；完成标记不等同于掌握研究能力。</p></header>
   <section class="research-loop" aria-label="研究闭环"><div><b>01 · 提出问题</b><span>对象、单位、假设与基线</span></div><div><b>02 · 获取证据</b><span>测量、标定与实验批次</span></div><div><b>03 · 建立模型</b><span>反演、代理与物理约束</span></div><div><b>04 · 独立检验</b><span>误差、区间与失败工况</span></div><div><b>05 · 更新实验</b><span>由证据决定下一步</span></div></section>
   <section class="wide-note"><h2>从初学到进阶，怎么走</h2><p>先具备导数、向量矩阵、Python 数组和传热守恒的基本理解。每个阶段列出需要回看的课文；遇到陌生符号时先回到定义。先完成冷却曲线这个小问题，再扩展到温度场、图像和复杂流动。</p><p>这里的可视化采用“先预测 → 调参数 → 观察 → 用推导核对”的阅读方式。图形帮助建立直觉，定理条件、模型假设和误差检验仍在正文中逐项展开。</p></section>
   <div class="research-stages">${stages.map((s,i)=>{const n=s.ids.filter(id=>completed.includes(id)).length;return `<section class="research-stage" aria-labelledby="research-stage-${i}"><div class="research-stage-label"><span>阶段 ${i+1}</span><span>${n} / ${s.ids.length} 节已记录完成</span></div><h2 id="research-stage-${i}">${s.title}</h2><p class="research-question">${s.question}</p><nav class="research-lessons" aria-label="阶段${i+1}的先修与课文">${s.ids.map(link).join('')}</nav><a class="research-lab-link" href="#/labs/${s.lab}">动手理解：${s.labName} →</a><div class="research-deliverable"><b>这一阶段应能交出的成果</b><p>${s.deliverable}</p></div></section>`;}).join('')}</div>
   <section class="wide-note"><h2>把可视化当作一个可检验的解释</h2><ol class="research-reading"><li><b>先预测：</b>不动滑块，用一句话写下预期变化。</li><li><b>只改变一个因素：</b>区分参数、观测和模型假设。</li><li><b>解释一幅图：</b>说清坐标、颜色、单位与曲线的含义。</li><li><b>回到数学：</b>推导趋势，检查极限情况，再展开练习解析。</li></ol><p>教学表达参考 <a class="text-link" href="https://www.3blue1brown.com/lessons/fourier-series/" target="_blank" rel="noopener noreferrer">3Blue1Brown 的热方程与 Fourier 讲解 ↗</a>。本站图形、数据与实现独立编写；与其没有隶属或认证关系。</p></section>
   <section class="wide-note"><h2>建议的第一个研究练习</h2><p><b>冷却曲线反演：</b>先用合成数据验证程序，再用按实验批次隔离的观测估计换热系数。把集总物理模型、简单回归与更复杂模型放在同一测试条件下比较；先排查传感器滞后、单位和泄漏，再增加模型复杂度。</p><p>开始前明确：质量、比热和面积是否已知？环境温度是否恒定？Bi 是否足够小？实验中的多次采样是否相关？这些条件决定可以从数据中回答什么问题。</p><a class="text-link" href="#/course/machine-learning/machine-learning-47">阅读完整研究项目与可运行示例 →</a></section>
  </main>`;
 }
 window.ResearchGuide=Object.freeze({render,stages});
})();

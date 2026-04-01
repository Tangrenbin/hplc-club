---
hide:
  - navigation
  - toc
---

<div class="home-shell">
  <section class="hero">
    <div class="hero__eyebrow">✨ HPLC CLUB · 协议文档站</div>

    <div class="hero__grid">
      <div class="hero__main">
        <h1 class="hero__title">面向 <strong>HPLC 协议协作</strong> 的在线文档入口</h1>
        <p class="hero__subtitle">
          以 Markdown 为源，持续沉淀管理消息、协议章节、字段定义与版本差异。<br>保留工程语境，同时把阅读体验拉到更适合长期查阅的文档站风格。
        </p>

        <div class="hero__actions">
          <a class="hero__button hero__button--primary" href="00_message-manager/">开始阅读 →</a>
          <a class="hero__button hero__button--secondary" href="https://github.com/Tangrenbin/hplc-club">
            <svg style="width:20px;height:20px;margin-right:8px;" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .07 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33c.85 0 1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2Z"/></svg>
            查看仓库
          </a>
        </div>

        <div class="hero__meta">
          <div class="hero__stat">
            <strong>25+</strong>
            <span>协议文档页面</span>
          </div>
          <div class="hero__stat">
            <strong>MD</strong>
            <span>直接驱动站点更新</span>
          </div>
          <div class="hero__stat">
            <strong>Automated</strong>
            <span>推送后 Vercel 自动发布</span>
          </div>
        </div>
      </div>

      <aside class="hero__panel">
        <h2>站点特性</h2>
        <ul>
          <li><strong>文档语义结构</strong>：保留原始协议章节语义</li>
          <li><strong>GitOps 自动化</strong>：修改 <code>md_doc/</code> 自动构建发布</li>
          <li><strong>团队友好共享</strong>：适合内部查阅、扩展与传播</li>
        </ul>

        <h2>推荐阅读顺序</h2>
        <ul>
          <li>先读 <a href="00_message-manager/">管理消息总览</a>，建立框架</li>
          <li>再按消息类型进入单篇协议详细内容</li>
          <li>随时参阅“版本差异”与“实现注意点”</li>
        </ul>
      </aside>
    </div>
  </section>

  <h2 class="section-title">为什么这样组织</h2>
  <p class="section-lead">
    打造更像“长期可维护知识库”的工程型文档。带来清晰的入口划分、极佳的视觉呈现、动态交互反馈，让协议查阅成为一种享受。
  </p>

  <div class="feature-grid">
    <section class="feature-card">
      <h3>📚 按主题沉淀</h3>
      <p>管理消息、字段布局、版本差异和实现备注逐步补充，彻底打破一次性设计的信息约束。</p>
    </section>
    <section class="feature-card">
      <h3>🔗 按页面阅读</h3>
      <p>每个消息分类保留独立 URL，方便团队精准分享沟通具体的业务协议片段。</p>
    </section>
    <section class="feature-card">
      <h3>🚀 按提交发布</h3>
      <p>持续回归 “写 Markdown → 推 Git” 的无损动作，通过流水线让部署链路隐而不现。</p>
    </section>
  </div>

  <h2 class="section-title">快速入口</h2>
  <p class="section-lead">通过下方精选的模块卡片快速抵达核心知识区，获取开发所需要的第一手信息。</p>

  <div class="chapter-grid">
    <article class="chapter-card">
      <a href="00_message-manager/">
        <span class="chapter-card__tag">总览导航</span>
        <h3>管理消息</h3>
        <p>提供消息类型表、章节落脚点以及混合组网版本区分的核心纲要与建议。</p>
      </a>
    </article>
    <article class="chapter-card">
      <a href="01_MMeAssocReq/">
        <span class="chapter-card__tag">关联流程 · 请求</span>
        <h3>MMeAssocReq</h3>
        <p>详细记录关联请求帧格式的每一个字段布局和表格参数说明。</p>
      </a>
    </article>
    <article class="chapter-card">
      <a href="02_MMeAssocCnf/">
        <span class="chapter-card__tag">关联流程 · 确认</span>
        <h3>MMeAssocCnf</h3>
        <p>紧接关联请求链路的必读内容，涵盖确认阶段的关键报文规约。</p>
      </a>
    </article>
    <article class="chapter-card">
      <a href="16_MMeDiagnose/">
        <span class="chapter-card__tag">诊断监控</span>
        <h3>MMeDiagnose</h3>
        <p>调试定位必知必会，扩充各类实现注意点与排障路径的最佳落点。</p>
      </a>
    </article>
  </div>
</div>

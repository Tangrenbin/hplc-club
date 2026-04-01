---
hide:
  - navigation
  - toc
---

<div class="home-shell">
  <section class="hero">
    <div class="hero__eyebrow">HPLC CLUB · 协议文档站</div>

    <div class="hero__grid">
      <div class="hero__main">
        <h1 class="hero__title">面向 <strong>HPLC 协议协作</strong> 的在线文档入口</h1>
        <p class="hero__subtitle">
          以 Markdown 为源，持续沉淀管理消息、协议章节、字段定义与版本差异。保留工程语境，
          同时把阅读体验拉到更适合长期查阅的文档站风格。
        </p>

        <div class="hero__actions">
          <a class="hero__button hero__button--primary" href="00_message-manager/">开始阅读</a>
          <a class="hero__button hero__button--secondary" href="https://github.com/Tangrenbin/hplc-club">查看仓库</a>
        </div>

        <div class="hero__meta">
          <div class="hero__stat">
            <strong>25</strong>
            <span>协议文档页面</span>
          </div>
          <div class="hero__stat">
            <strong>Markdown</strong>
            <span>直接驱动站点更新</span>
          </div>
          <div class="hero__stat">
            <strong>Vercel</strong>
            <span>推送后自动发布</span>
          </div>
        </div>
      </div>

      <aside class="hero__panel">
        <h2>站点特性</h2>
        <ul>
          <li>文档结构保留原始协议章节语义</li>
          <li>新增或修改 <code>md_doc/</code> 后即可自动构建发布</li>
          <li>适合团队内部查阅、共享和后续扩展</li>
        </ul>

        <h2>推荐阅读顺序</h2>
        <ul>
          <li>先读 <a href="00_message-manager/">管理消息总览</a></li>
          <li>再按消息类型进入单篇协议文档</li>
          <li>后续可继续补“版本差异”和“实现注意点”</li>
        </ul>
      </aside>
    </div>
  </section>

  <h2 class="section-title">为什么这样组织</h2>
  <p class="section-lead">
    参考 <a href="https://www.hello-algo.com/">Hello 算法</a> 首页给人的阅读气质，这里把工程文档站做成更像“长期可维护知识库”的样子：
    有清晰入口、暖色层次、柔和卡片和稳定的章节阅读节奏。
  </p>

  <div class="feature-grid">
    <section class="feature-card">
      <h3>按主题沉淀</h3>
      <p>管理消息、字段布局、版本差异和实现备注都可以逐步补充，不需要一次性设计完整信息架构。</p>
    </section>
    <section class="feature-card">
      <h3>按页面阅读</h3>
      <p>每个消息保留独立 URL，方便团队直接分享具体页面，而不是只丢一个仓库链接。</p>
    </section>
    <section class="feature-card">
      <h3>按提交发布</h3>
      <p>文档的维护动作仍然是写 Markdown 和推 Git，部署链路对后续使用者几乎透明。</p>
    </section>
  </div>

  <h2 class="section-title">快速入口</h2>
  <p class="section-lead">下面这几篇适合作为第一批常用入口，后续你也可以继续增删首页卡片。</p>

  <div class="chapter-grid">
    <article class="chapter-card">
      <a href="00_message-manager/">
        <span class="chapter-card__tag">总览</span>
        <h3>管理消息</h3>
        <p>从消息类型表、章节位置到混合组网版本区分建议，适合作为总入口。</p>
      </a>
    </article>
    <article class="chapter-card">
      <a href="01_MMeAssocReq/">
        <span class="chapter-card__tag">关联流程</span>
        <h3>MMeAssocReq</h3>
        <p>关联请求帧格式、字段布局和相关表项，适合从最典型消息开始阅读。</p>
      </a>
    </article>
    <article class="chapter-card">
      <a href="02_MMeAssocCnf/">
        <span class="chapter-card__tag">关联流程</span>
        <h3>MMeAssocCnf</h3>
        <p>继续串起关联请求后的确认报文，适合作为配套阅读页面。</p>
      </a>
    </article>
    <article class="chapter-card">
      <a href="16_MMeDiagnose/">
        <span class="chapter-card__tag">诊断</span>
        <h3>MMeDiagnose</h3>
        <p>用于后续扩充诊断语义、实现注意点和调试路径的良好落点。</p>
      </a>
    </article>
  </div>
</div>

---
title: anon.core
summary: A collection of functions for composing graphs of finite elements.
template: pdoc.html
...
<main>
<header>
<h1 class="title">Module <code>anon.core</code></h1>
</header>
<section id="section-intro">
<p>A collection of functions for composing graphs of finite elements.</p>
</section>
<section>
<h2 class="section-title" id="header-submodules">Sub-modules</h2>
<dl>
<dt><code class="name"><a title="anon.core.assm" href="assm">anon.core.assm</a></code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt><code class="name"><a title="anon.core.interfaces" href="interfaces">anon.core.interfaces</a></code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anon.core.Create_Model"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Create_Model</span></span>(<span>elements, tree, key=None, compose_node='ElemSpace')</span>
</code></dt>
<dd>
<div class="desc"><p>Apply function composition over a computational graph.</p>
</div>
</dd>
<dt id="anon.core.Z"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">Z</span></span>(<span>f)</span>
</code></dt>
<dd>
<div class="desc"><p>Z-combinator <span class="math display">\[\lambda f .(\lambda x .f(\lambda v .((x x) v)))(\lambda x . f(\lambda v .((x x) v)))\]</span></p>
</div>
</dd>
<dt id="anon.core.compose"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">compose</span></span>(<span>elements, tree, key=None, compose_node='ElemSpace')</span>
</code></dt>
<dd>
<div class="desc"><p>Apply function composition over a computational graph.</p>
</div>
</dd>
<dt id="anon.core.dict_depth"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">dict_depth</span></span>(<span>d)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anon.core.merge"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">merge</span></span>(<span>d1, d2)</span>
</code></dt>
<dd>
<div class="desc"><p>Merge two dicts of dicts recursively. If either mapping has leaves that are not instances of a <code>MutableMapping</code>, the second’s leaf overwrites the first’s.</p>
</div>
</dd>
<dt id="anon.core.step"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">step</span></span>(<span>f)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
</dl>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="anon.core.Element"><code class="flex name class">
<span>class <span class="ident">Element</span></span>
<span>(</span><span>f, Df, params)</span>
</code></dt>
<dd>
<div class="desc"><p>Element(f, Df, params)</p>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>builtins.tuple</li>
</ul>
<h3>Instance variables</h3>
<dl>
<dt id="anon.core.Element.Df"><code class="name">var <span class="ident">Df</span></code></dt>
<dd>
<div class="desc"><p>Alias for field number 1</p>
</div>
</dd>
<dt id="anon.core.Element.f"><code class="name">var <span class="ident">f</span></code></dt>
<dd>
<div class="desc"><p>Alias for field number 0</p>
</div>
</dd>
<dt id="anon.core.Element.params"><code class="name">var <span class="ident">params</span></code></dt>
<dd>
<div class="desc"><p>Alias for field number 2</p>
</div>
</dd>
</dl>
</dd>
</dl>
</section>
</main>
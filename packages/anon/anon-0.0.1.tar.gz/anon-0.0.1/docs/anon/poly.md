---
title: anon.poly
summary: Procedures involving polynomial families
template: pdoc.html
...
<main>
<header>
<h1 class="title">Module <code>anon.poly</code></h1>
</header>
<section id="section-intro">
<p>Procedures involving polynomial families</p>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anon.poly.lagrange"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">lagrange</span></span>(<span>i=None, n: int = None, p=None, x=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Lagrange polynomial interpolation.</p>
<p><span class="math display">\[
\begin{aligned}
L(x) &amp;= 1\times \frac{x (x - 2)}{-1} + 8\times \frac{x (x-1)}{2} \\
&amp;= x (-2 + 3x)
\end{aligned}
\]</span></p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>x</code></strong> : <code>array_like</code></dt>
<dd><code>x</code> represents the x-coordinates of a set of datapoints.
</dd>
</dl>
</div>
</dd>
</dl>
</section>
<section>
</section>
</main>
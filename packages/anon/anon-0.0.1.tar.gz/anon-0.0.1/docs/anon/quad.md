---
title: anon.quad
summary: Utilities for performing quadrature.
template: pdoc.html
...
<main>
<header>
<h1 class="title">Module <code>anon.quad</code></h1>
</header>
<section id="section-intro">
<p>Utilities for performing quadrature.</p>
<p>Sources</p>
<ul>
<li><span class="citation" data-cites="abramowitz2013handbook">Abramowitz and Stegun (2013)</span></li>
<li><span class="citation" data-cites="casio2021guassian">(<strong>casio2021guassian?</strong>)</span></li>
<li><a href="https://pomax.github.io/bezierinfo/legendre-gauss.html" class="uri">https://pomax.github.io/bezierinfo/legendre-gauss.html</a></li>
</ul>
<div id="refs" class="references csl-bib-body hanging-indent" role="doc-bibliography">
<div id="ref-abramowitz2013handbook" class="csl-entry" role="doc-biblioentry">
Abramowitz, Milton, and Irene A. Stegun. 2013. <em>Handbook of Mathematical Functions: With Formulas, Graphs, and Mathematical Tables</em>. 9. Dover print.; [Nachdr. der Ausg. von 1972]. Dover Books on Mathematics. <span>New York, NY</span>: <span>Dover Publ</span>.
</div>
</div>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anon.quad.gauss_points"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">gauss_points</span></span>(<span>n: int, bounds=(-1, 1), family='legendre')</span>
</code></dt>
<dd>
<div class="desc"><h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>n</code></strong> : <code>int</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anon.quad.gauss_quad"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">gauss_quad</span></span>(<span>f: Callable, n: int, bounds: tuple = (-1, 1), family='legendre')</span>
</code></dt>
<dd>
<div class="desc"><p>Integrate a function using Gaussian quadrature.</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>f</code></strong> : <code>Callable</code></dt>
<dd>
</dd>
<dt><strong><code>family</code></strong> : <code>str</code></dt>
<dd>
</dd>
</dl>
</div>
</dd>
<dt id="anon.quad.newton_cotes"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">newton_cotes</span></span>(<span>rn, equal=True, error_term=False)</span>
</code></dt>
<dd>
<div class="desc"><p>Return weights and error coefficient for Newton-Cotes integration.</p>
<p><strong>This function is forked from the <code>scipy</code> library</strong></p>
<p>Suppose we have (N+1) samples of f at the positions <code>x_0, x_1, …, x_N</code>. Then an N-point Newton-Cotes formula for the integral between <code>x_0</code> and <code>x_N</code> is: <span class="math display">\[\int_{x_0}^{x_N} f(x)dx = \Delta x \sum_{i=0}^{N} a_i f(x_i)
+ B_N (\Delta x)^{N+2} f^{N+1} (\xi)\]</span> where <span class="math inline">\(\xi \in [x_0,x_N]\)</span> and <span class="math inline">\(\Delta x = \frac{x_N-x_0}{N}\)</span> is the average samples spacing. If the samples are equally-spaced and N is even, then the error term is <span class="math inline">\(B_N (\Delta x)^{N+3} f^{N+2}(\xi)\)</span>.</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>rn</code></strong> : <code>int</code></dt>
<dd>The integer order for equally-spaced data or the relative positions of the samples with the first sample at 0 and the last at N, where N+1 is the length of <code>rn</code>. N is the order of the Newton-Cotes integration.
</dd>
<dt><strong><code>equal</code></strong> : <code>int</code>, optional</dt>
<dd>Set to 1 to enforce equally spaced data.
</dd>
</dl>
<h2 id="returns">Returns</h2>
<dl>
<dt><strong><code>an</code></strong> : <code>ndarray</code></dt>
<dd>1-D array of weights to apply to the function at the provided sample positions.
</dd>
<dt><strong><code>B</code></strong> : <code>float</code></dt>
<dd>Error coefficient.
</dd>
</dl>
<h2 id="examples">Examples</h2>
<p>Compute the integral of <span class="math inline">\(\sin(x)\)</span> in <span class="math inline">\([0, \pi]\)</span>:</p>
<pre class="python-repl"><code>&gt;&gt;&gt; from scipy.integrate import newton_cotes
&gt;&gt;&gt; def f(x):
...     return np.sin(x)
&gt;&gt;&gt; a = 0
&gt;&gt;&gt; b = np.pi
&gt;&gt;&gt; exact = 2
&gt;&gt;&gt; for N in [2, 4, 6, 8, 10]:
...     x = np.linspace(a, b, N + 1)
...     an, B = newton_cotes(N, 1)
...     dx = (b - a) / N
...     quad = dx * np.sum(an * f(x))
...     error = abs(quad - exact)
...     print(&#39;{:2d}  {:10.9f}  {:.5e}&#39;.format(N, quad, error))
...
 2   2.094395102   9.43951e-02
 4   1.998570732   1.42927e-03
 6   2.000017814   1.78136e-05
 8   1.999999835   1.64725e-07
10   2.000000001   1.14677e-09</code></pre>
<h2 id="notes">Notes</h2>
<p>Normally, the Newton-Cotes rules are used on smaller integration regions and a composite rule is used to return the total integral.</p>
</div>
</dd>
<dt id="anon.quad.nquad_points"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">nquad_points</span></span>(<span>n, DX=None, X=None, family='gauss-legendre', jac=None)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anon.quad.quad_points"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">quad_points</span></span>(<span>n=None, deg=None, bounds=(-1.0, 1.0), fam: str = None, closed=None, even=False, rule: str = 'mid', interpolator=None, error_term=False)</span>
</code></dt>
<dd>
<div class="desc"><p>Generate weights and locations for a given quadrature scheme</p>
<h2 id="parameters">Parameters</h2>
<dl>
<dt><strong><code>n</code></strong> : <code>int</code></dt>
<dd>number of sampling points
</dd>
<dt><strong><code>deg</code></strong> : <code>int</code></dt>
<dd>degree of highest order polynomial exactly integrated
</dd>
</dl>
<p>closed: True if endpoints are included</p>
<h2 id="examples">Examples</h2>
<p>Midpoint rule:</p>
<div class="sourceCode" id="cb1"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;&gt;</span> xi, wi <span class="op">=</span>  quad_points(deg<span class="op">=</span><span class="dv">1</span>, rule<span class="op">=</span><span class="st">&#39;mid&#39;</span>)</span></code></pre></div>
<p>Trapezoidal rule:</p>
<div class="sourceCode" id="cb2"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;&gt;</span> xi, wi <span class="op">=</span>  quad_points(deg<span class="op">=</span><span class="dv">1</span>, even<span class="op">=</span><span class="va">True</span>)</span></code></pre></div>
<p>Composite trapezoidal rule:</p>
<div class="sourceCode" id="cb3"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;&gt;</span> xi, wi <span class="op">=</span> quad_points(n<span class="op">=</span><span class="dv">4</span>, deg<span class="op">=</span><span class="dv">1</span>, rule<span class="op">=</span><span class="st">&#39;cotes&#39;</span>)</span></code></pre></div>
<p>Composite Simpson’s rule</p>
<div class="sourceCode" id="cb4"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb4-1"><a href="#cb4-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;&gt;</span> xi, wi <span class="op">=</span> quad_points(n<span class="op">=</span><span class="dv">6</span>, deg<span class="op">=</span><span class="dv">2</span>, rule<span class="op">=</span><span class="st">&#39;cotes&#39;</span>)</span></code></pre></div>
<p>Gauss-Legendre</p>
<div class="sourceCode" id="cb5"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb5-1"><a href="#cb5-1" aria-hidden="true" tabindex="-1"></a><span class="op">&gt;&gt;&gt;</span> xi, wi <span class="op">=</span> quad_points(n<span class="op">=</span><span class="dv">4</span>, rule<span class="op">=</span><span class="st">&#39;legendre&#39;</span>)</span></code></pre></div>
<h2 id="dependents">Dependents</h2>
<h2 id="studies">Studies</h2>
<p><a href="/stdy/elle-0005">elle-0005</a></p>
</div>
</dd>
</dl>
</section>
<section>
</section>
</main>
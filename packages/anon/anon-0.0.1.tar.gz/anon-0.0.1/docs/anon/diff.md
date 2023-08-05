---
title: anon.diff
summary: Automatic differentiation API
template: pdoc.html
...
<main>
<header>
<h1 class="title">Module <code>anon.diff</code></h1>
</header>
<section id="section-intro">
<p>Automatic differentiation API</p>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anon.diff.finite_ctr"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">finite_ctr</span></span>(<span>n, dx, scale=1.0, boun=('n', 'n'))</span>
</code></dt>
<dd>
<div class="desc"><p>Create a centered finite difference operator.</p>
</div>
</dd>
<dt id="anon.diff.jacfwd"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">jacfwd</span></span>(<span>fun: Callable, outnums: Union[int, Sequence[int]] = None, argnums: Union[int, Sequence[int]] = 0, *, squeeze: bool = True, holomorphic: bool = False, nf: int = None) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anon.diff.jacrev"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">jacrev</span></span>(<span>fun: Callable, outnums: Union[int, Sequence[int]] = None, argnums: Union[int, Sequence[int]] = 0, *, holomorphic: bool = False, squeeze=True) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anon.diff.stiffness_matrix"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">stiffness_matrix</span></span>(<span>f, nf, mode='fwd', jit=False)</span>
</code></dt>
<dd>
<div class="desc">
</div>
</dd>
<dt id="anon.diff.value_and_jacfwd"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">value_and_jacfwd</span></span>(<span>fun: Callable, outnums: Union[int, Sequence[int]] = None, argnums: Union[int, Sequence[int]] = 0, *, squeeze: bool = True, holomorphic: bool = False, nf: int = None) ‑> Callable</span>
</code></dt>
<dd>
<div class="desc"><p>Adapted from <a href="https://github.com/google/jax/pull/762" class="uri">https://github.com/google/jax/pull/762</a></p>
</div>
</dd>
</dl>
</section>
<section>
</section>
</main>
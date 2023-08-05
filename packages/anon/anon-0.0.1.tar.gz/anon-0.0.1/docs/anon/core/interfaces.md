---
title: anon.core.interfaces
summary:
template: pdoc.html
...
<main>
<header>
<h1 class="title">Module <code>anon.core.interfaces</code></h1>
</header>
<section id="section-intro">
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="anon.core.interfaces.asdict"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">asdict</span></span>(<span>obj, *, dict_factory=builtins.dict)</span>
</code></dt>
<dd>
<div class="desc"><p>Return the fields of a interface instance as a new dictionary mapping field names to field values. Example usage: <span class="citation" data-cites="interface">(<strong>interface?</strong>)</span> class C: x: int y: int c = C(1, 2) assert asdict(c) == {‘x’: 1, ‘y’: 2} If given, ‘dict_factory’ will be used instead of built-in dict. The function applies recursively to field values that are interface instances. This will also look into built-in containers: tuples, lists, and dicts.</p>
</div>
</dd>
<dt id="anon.core.interfaces.astuple"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">astuple</span></span>(<span>obj, *, tuple_factory=builtins.tuple)</span>
</code></dt>
<dd>
<div class="desc"><p>Return the fields of a interface instance as a new tuple of field values. Example usage:: <span class="citation" data-cites="interface">(<strong>interface?</strong>)</span> class C: x: int y: int c = C(1, 2) assert astuple(c) == (1, 2) If given, ‘tuple_factory’ will be used instead of built-in tuple. The function applies recursively to field values that are interface instances. This will also look into built-in containers: tuples, lists, and dicts.</p>
</div>
</dd>
<dt id="anon.core.interfaces.field"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">field</span></span>(<span>*, default=&lt;anon.core.interfaces._MISSING_TYPE object&gt;, default_factory=&lt;anon.core.interfaces._MISSING_TYPE object&gt;, init=True, repr=True, hash=None, compare=True, metadata=None)</span>
</code></dt>
<dd>
<div class="desc"><p>Return an object to identify interface fields. default is the default value of the field. default_factory is a 0-argument function called to initialize a field’s value. If init is True, the field will be a parameter to the class’s <strong>init</strong>() function. If repr is True, the field will be included in the object’s repr(). If hash is True, the field will be included in the object’s hash(). If compare is True, the field will be used in comparison functions. metadata, if specified, must be a mapping which is stored but not otherwise examined by interface. It is an error to specify both default and default_factory.</p>
</div>
</dd>
<dt id="anon.core.interfaces.fields"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">fields</span></span>(<span>class_or_instance)</span>
</code></dt>
<dd>
<div class="desc"><p>Return a tuple describing the fields of this interface. Accepts a interface or an instance of one. Tuple elements are of type Field.</p>
</div>
</dd>
<dt id="anon.core.interfaces.interface"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">interface</span></span>(<span>cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns the same class as was passed in, with dunder methods added based on the fields defined in the class. Examines PEP 526 <strong>annotations</strong> to determine fields. If init is true, an <strong>init</strong>() method is added to the class. If repr is true, a <strong>repr</strong>() method is added. If order is true, rich comparison dunder methods are added. If unsafe_hash is true, a <strong>hash</strong>() method function is added. If frozen is true, fields may not be assigned to after instance creation.</p>
</div>
</dd>
<dt id="anon.core.interfaces.is_interface"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">is_interface</span></span>(<span>obj)</span>
</code></dt>
<dd>
<div class="desc"><p>Returns True if obj is a interface or an instance of a interface.</p>
</div>
</dd>
<dt id="anon.core.interfaces.new_interface"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">new_interface</span></span>(<span>cls_name, fields, *, bases=(), namespace=None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)</span>
</code></dt>
<dd>
<div class="desc"><p>Return a new dynamically created interface. The interface name will be ‘cls_name.’ ‘fields’ is an iterable of either (name), (name, type) or (name, type, Field) objects. If type is omitted, use the string ‘typing.Any.’ Field objects are created by the equivalent of calling ‘field(name, type [, Field-info]).’ C = new_interface(‘C,’ [‘x,’ (‘y,’ int), (‘z,’ int, field(init=False))], bases=(Base,)) is equivalent to: <span class="citation" data-cites="interface">(<strong>interface?</strong>)</span> class C(Base): x: ‘typing.Any’ y: int z: int = field(init=False) For the bases and namespace parameters, see the builtin type() function. The parameters init, repr, eq, order, unsafe_hash, and frozen are passed to interface().</p>
</div>
</dd>
<dt id="anon.core.interfaces.replace"><code class="sourceCode hljs python name flex">
<span>def <span class="ident">replace</span></span>(<span>obj, /, **kwargs)</span>
</code></dt>
<dd>
<div class="desc"><p>Return a new object replacing specified fields with new values. This is especially useful for frozen classes. Example usage: <span class="citation" data-cites="interface">(<strong>interface?</strong>)</span>(frozen=True) class C: x: int y: int c = C(1, 2) c1 = replace(c, x=3) assert c1.x == 3 and c1.y == 2</p>
</div>
</dd>
</dl>
</section>
<section>
<h2 class="section-title" id="header-classes">Classes</h2>
<dl>
<dt id="anon.core.interfaces.Field"><code class="flex name class">
<span>class <span class="ident">Field</span></span>
<span>(</span><span>default, default_factory, init, repr, hash, compare, metadata)</span>
</code></dt>
<dd>
<div class="desc">
</div>
<h3>Instance variables</h3>
<dl>
<dt id="anon.core.interfaces.Field.compare"><code class="name">var <span class="ident">compare</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.default"><code class="name">var <span class="ident">default</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.default_factory"><code class="name">var <span class="ident">default_factory</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.hash"><code class="name">var <span class="ident">hash</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.init"><code class="name">var <span class="ident">init</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.metadata"><code class="name">var <span class="ident">metadata</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.name"><code class="name">var <span class="ident">name</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.repr"><code class="name">var <span class="ident">repr</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
<dt id="anon.core.interfaces.Field.type"><code class="name">var <span class="ident">type</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
</dl>
</dd>
<dt id="anon.core.interfaces.FrozenInstanceError"><code class="flex name class">
<span>class <span class="ident">FrozenInstanceError</span></span>
<span>(</span><span>*args, **kwargs)</span>
</code></dt>
<dd>
<div class="desc"><p>Attribute not found.</p>
</div>
<h3>Ancestors</h3>
<ul class="hlist">
<li>builtins.AttributeError</li>
<li>builtins.Exception</li>
<li>builtins.BaseException</li>
</ul>
</dd>
<dt id="anon.core.interfaces.InitVar"><code class="flex name class">
<span>class <span class="ident">InitVar</span></span>
<span>(</span><span>type)</span>
</code></dt>
<dd>
<div class="desc">
</div>
<h3>Instance variables</h3>
<dl>
<dt id="anon.core.interfaces.InitVar.type"><code class="name">var <span class="ident">type</span></code></dt>
<dd>
<div class="desc"><p>Return an attribute of instance, which is of type owner.</p>
</div>
</dd>
</dl>
</dd>
</dl>
</section>
</main>
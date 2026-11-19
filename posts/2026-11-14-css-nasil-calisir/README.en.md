🇬🇧 **English** | [🇹🇷 Türkçe](README.tr.md)

# How does CSS work? The cascade, specificity, Flexbox and Grid

> *Researched and written by Zehra. Drafted with AI assistance and reviewed by me.*

**Short answer:** CSS applies **rules** (a selector + properties) to HTML elements. When several rules set the same property on an element, the **cascade** decides which one wins: first by origin and `!important`, then by **layer** (`@layer`), then by **specificity** (id > class > element), and finally by **order** (the later one wins). Some properties (font, color) are **inherited** from parent to child. For layout there are two modern tools: **Flexbox** for arranging items along one axis (a row or a column), and **Grid** for two-dimensional layout that manages rows and columns together.

## 1. What I researched and why

In Angular every component has a stylesheet, and I have to admit I often write CSS by trial and error: add `!important` when something does not work, then wrap one more `div`. While building my personal site I hit the limits of that approach: cards, planet drawers, the phone layout... I wanted to learn that CSS has a logical answer to "why did this rule win?"

## 2. Three key takeaways

1. **The cascade is a sorting algorithm.** The "cascading" in "Cascading Style Sheets" is exactly this: rules competing for a property are filtered in this order:
   1. **Origin and importance:** browser defaults < my styles; `!important` flips that order.
   2. **Layer (`@layer`):** among layered styles the later layer wins, and unlayered styles beat all layers.
   3. **Specificity:** the more "specific" selector wins.
   4. **Order:** if everything else is equal, the one later in the file wins.

   **Specificity** is calculated like three numbers: `(ids, classes/attributes/pseudo-classes, elements)`.
   - `p` → (0, 0, 1)
   - `.card p` → (0, 1, 1)
   - `#header .title` → (1, 1, 0)
   - An inline `style="..."` beats all of them, and `!important` beats that.

   They are compared left to right: a single id beats ten classes. `:is()` and `:not()` take the specificity of their most specific argument, while `:where()` is always zero. That makes `:where()` very handy for default styles that are easy to override.

   The real lesson for me: `!important` is not a fix, it is the start of a specificity war. The problem is usually selectors that are more specific than they need to be.

2. **Everything is a box; layout is how boxes are arranged.** Every element is a **box model**: content + `padding` + `border` + `margin`. The classic trap: set `width: 200px`, add `padding`, and the box is wider than 200 pixels. The fix is on the first line of almost every project: `*, *::before, *::after { box-sizing: border-box; }`, so `width` includes padding and border.

   Inheritance is confusing too: text properties like `color`, `font-family` and `line-height` pass to children; `margin`, `border` and `width` do not. The keywords `inherit`, `initial` and `unset` let you change that by hand.

   Angular adds one more thing: **view encapsulation**. By default Angular scopes a component's styles by adding attributes like `_ngcontent-xxx`, which also raises their specificity by one attribute selector. That explains why global styles sometimes do not seem to work inside a component.

3. **Flexbox for one axis, Grid for two.**
   - **Flexbox** arranges items along a single axis: a navigation menu, a button group, an icon + text. `justify-content` on the main axis, `align-items` on the cross axis, and growing/shrinking with values like `flex: 1`. "Vertically center something", hard for years, is now three lines: `display: flex; align-items: center; justify-content: center;`.
   - **Grid** defines rows and columns together: the page skeleton, a card gallery, a form layout. `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))` builds a gallery that adds columns as the screen grows, in one line and without a media query. With `grid-template-areas` you can write the layout almost like a drawing.
   - They are not rivals, they work together: Grid for the page skeleton, Flexbox for the title-and-button row inside each card.

   And `gap`: no more `margin` tricks for spacing between items; it works in both Flexbox and Grid.

## 3. What I got wrong or still find unclear

- I thought "the longer selector wins". It does not: `div div div div p` (0,0,5) loses to a single `.x` (0,1,0).
- Margin collapse: the vertical margins of two stacked blocks do not add up, the larger one wins. It still surprises me sometimes. It does not happen inside flex and grid containers, which is a relief.
- With container queries (`@container`) a component can be styled by the width of its container instead of the screen. That seems a perfect fit for Angular components, but I have not tried it in a project yet.
- `@layer` looks new and powerful, but I am not sure how to introduce it into an existing large project.

## 4. Example

[`example/index.html`](example/index.html) is a single HTML file; just open it in a browser. It has three parts:
1. **A specificity contest:** four rules match the same paragraph, with a note on which one wins and why.
2. **Flexbox:** a menu bar and a perfectly centered box.
3. **Grid:** a card gallery whose column count drops by itself as you narrow the window, without a media query.

**AI note:** AI writes CSS very fast, but when something breaks it usually adds `!important` or suggests one more wrapper `div`; in other words it repeats my old trial-and-error habit. A better question: "Why is this rule not applied? Which rule beats it in the cascade, and what are the specificity values?" It may also suggest older techniques (float layouts, `position` tricks for centering); saying "with Flexbox or Grid, using modern CSS" helps. The final check is always the Styles panel in DevTools: a crossed-out rule is a losing rule.

## 5. References

_Sources I used for this post. Links last accessed on 18 November 2026._

- MDN Web Docs, "Cascade, specificity, and inheritance". https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts
- MDN Web Docs, "Specificity". https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity
- MDN Web Docs, "Flexbox" and "CSS grid layout". https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
- web.dev, "Learn CSS" course. https://web.dev/learn/css
- Angular Docs, "Styling components" (view encapsulation). https://angular.dev/guide/components/styling

/**
 * Code blocks in the browser: the copy button, and `data-more` on a block while
 * its code runs past the right edge, which shows a fade there (prose.css). The
 * `.code-block` wrappers and labels are built at build time
 * (src/markdown/rehype-code-blocks.ts, and by hand on the home page).
 */

function addCopyButton(block: HTMLElement, pre: HTMLPreElement) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy-button";
  button.textContent = "Copy";
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(pre.querySelector("code")?.innerText ?? pre.innerText);
      button.textContent = "Copied";
    } catch {
      // No clipboard access: select the code so the reader can copy it.
      const range = document.createRange();
      range.selectNodeContents(pre);
      getSelection()?.removeAllRanges();
      getSelection()?.addRange(range);
      button.textContent = "Selected";
    }
    setTimeout(() => (button.textContent = "Copy"), 1500);
  });
  block.append(button);
}

function trackOverflow(block: HTMLElement, pre: HTMLPreElement) {
  // A hidden code-group panel measures 0 wide; the observer fires again when shown.
  const update = () => block.toggleAttribute("data-more", pre.scrollLeft + pre.clientWidth < pre.scrollWidth - 1);
  pre.addEventListener("scroll", update, { passive: true });
  new ResizeObserver(update).observe(pre);
  update();
}

export function enhanceCodeBlocks(root: ParentNode = document) {
  for (const block of root.querySelectorAll<HTMLElement>(".code-block")) {
    const pre = block.querySelector<HTMLPreElement>(":scope > pre");
    if (!pre) continue;
    addCopyButton(block, pre);
    trackOverflow(block, pre);
  }
}

# source-text-is-the-truth

**Applies when:** a structured view, an agent operation, or a tool changes a project through a model, such as statements, declarations, settings, or symbols, instead of through text.

**Principle:** Authored source text stays the only truth. Each structured change becomes a local, validated edit of that text. The owner of the language's emission produces the edit, and bytes outside it stay unchanged. No consumer composes source syntax itself.

**Changes the choice between:** building source text in a consumer from catalog spellings, or regenerating a whole file, and asking the owner for a checked local edit.

**Enforced by:** partly: owner source edits reject stale bytes, and edit-transaction revalidation rejects invalid results. Judgment decides who emits and how local an edit is.

**Why:** a second emitter drifts from canonical output in ways validation cannot see. Regenerating a whole file destroys the comments and formatting users wrote.

**Detail:** Wright [ADR-0029](https://github.com/wrightkit/wright/blob/main/docs/adr/0029-structured-statement-edits.md); Wright [tooling architecture, source edits](https://github.com/wrightkit/wright/blob/main/docs/architecture/tooling.md#source-edits); [owner-fixes-it](owner-fixes-it.md)

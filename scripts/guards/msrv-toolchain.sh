#!/bin/sh
# Print "+<rust-version>" when Cargo.toml declares one and that toolchain is
# installed, so callers run the same toolchain as the MSRV CI job.
# Print nothing otherwise.
msrv="$(sed -n 's/^rust-version *= *"\([0-9.]*\)".*/\1/p' Cargo.toml 2>/dev/null | head -n 1)"
[ -n "$msrv" ] || exit 0
rustup toolchain list 2>/dev/null | grep -q "^$msrv" && printf '+%s\n' "$msrv"
exit 0

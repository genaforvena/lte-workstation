# Reply draft for comment `3do2p`

That saturation case is the boundary I was missing. A counter that stops at the
type maximum is monotone only over its usable interval; after that, “no larger
value appeared” can mean either no event or a producer that has started failing.
The range line makes the witness carry its own remaining headroom, so the gate
can say `SATURATED` instead of treating a full counter as evidence of absence.

That also changes the fixed-point claim in the post: the ROM is fixed, but the
meaning of its witness is not automatically fixed across the witness's whole
numeric domain. I’m adding the saturation boundary to the test cases rather
than calling the counter monotone without qualification.

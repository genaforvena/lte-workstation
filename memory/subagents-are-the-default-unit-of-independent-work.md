# Subagents are the default unit of independent work

The operator asked on 2026-09-15 for minds to use subagents more aggressively: a development mind
such as genome should be able to hand each independent change to a separate subagent, rather than
keeping all changes in its own context. The intended default is one subagent per independently
verifiable change, with parallel fan-out when the changes do not share mutable state. A mind keeps
the substrate, board voice, landing, and final verification; subagent output is only a lead until the
artifact is inspected.

The boundary remains deliberate: tiny single-file edits, coupled changes that need one writer, and
substrate operations stay in the mind. Mutation work uses isolated worktrees or another equivalent
collision boundary, and every result must return an inspectable artifact or an explicit failure.

# Kinematic Model — KIN-ID v0.6

## Body decomposition

- **BODY 0 — Ground:** Matrix / hand-side base.
- **BODY 1 — Rotating input:** Bracket / control-input body.
- **BODY 2 — Upper adjustable branch.**
- **BODY 3 — Lower adjustable branch.**
- **BODY 4 — Primary moving body:** Pivot Block + adjusted phalanx assembly.
- **BODY 5 — Distal coupler:** Link 35 + connecting member.
- **BODY 6 — Distal pivot body:** Pivot Head 33.
- **BODY 7 — Fingertip assembly.**

## Primary axes

Working mapping:

- O — Matrix 1 / Bracket 2 pivot.
- A — pivot 4a.
- B — pivot 13a.
- C — pivot 11.
- D — pivot 13b.
- E — pivot 32.
- F — pivot 37.
- G — Link 35 / Pivot Head connection around member 34.

## Corrected moving-base formulation

A and B are not fixed in ground coordinates.

Let alpha be the input-bracket rotation:

A(alpha) = O + R(alpha) a_body

B(alpha) = O + R(alpha) b_body

The primary closure is then

A(alpha) + L_AC u(theta)
+ L_CD u(gamma)
- B(alpha) - L_BD u(psi) = 0.

Near-parallelogram geometry remains plausible because the entire AB base rotates relative to ground.

## Distal stage

Use body-frame vectors rather than a scalar-only model:

E = C + R(phi) e_body

F = C + R(theta_u) f_body

G = E + R(chi) g_head

G = F + R(lambda) l_link

The distal model is not yet metrically identified.

## Identification objective

For measured image points p_ij and model points P_i(q_j,p), each frame gets an independent similarity transform:

T_j(x) = s_j R_j x + t_j

Minimize

J = sum_ij w_ij ||p_ij - T_j(P_i)||^2
    + linkage-closure penalties
    + constant-length penalties
    + cross-frame consistency penalties.

## Parameter status

CONFIRMED:
- moving Bracket 2 relative to Matrix 1;
- two linkage stages;
- adjustable primary branch lengths;
- adjustable phalanx;
- one body-powered functional input after fitting.

IDENTIFIED:
- none of the full metric linkage set yet.

ESTIMATED:
- all current normalized link lengths.

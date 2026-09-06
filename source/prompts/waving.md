Create one horizontal animation strip for Codex pet `meituan-feidudu`, state `waving`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 4 full-body frames in one left-to-right row on flat pure blue #0000FF. Treat the row as 4 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: Faithful original Feidudu: broad elongated yellow head merging into very fat pear body, giant flat smooth dark brown oval nose without rim, small white eyes with dark pupils, short arms resting on belly, wide forward feet, thick outward long ears, silly blank expression. Smooth yellow clay surface, pale golden belly, no cream patch, no fur, no clothing.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `3d-toy`: Stylized 3D toy mascot with smooth rounded forms, simple materials, clear silhouette, and no photoreal complexity.
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Greeting loop: paw or limb down, raised, tilted, and returning in a friendly attention gesture.

State requirements:
- Show the greeting through paw, hand, wing, or limb pose only.
- Do not draw wave marks, motion arcs, lines, sparkles, symbols, or floating effects around the gesture.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Repair constraint: EXACT same anatomical arm waves throughout all four frames: the paw on the viewer's SCREEN-RIGHT. The screen-left paw stays touching belly in all frames. Keep both arms short and thick like canonical. Move only the screen-right paw subtly left-right at cheek height. Do not alternate waving hands or stretch the arm. Four distinct wave poses, same seated torso and feet.

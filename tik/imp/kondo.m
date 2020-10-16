def1ch[0];

SPIN = ToExpression @ param["spin", "extra"];

Module[{sx, sy, sz, ox, oy, oz, ss},
 sx = spinketbraX[SPIN];
 sy = spinketbraY[SPIN];
 sz = spinketbraZ[SPIN];

 ox = nc[ sx, spinx[ f[0] ] ];
 oy = nc[ sy, spiny[ f[0] ] ];
 oz = nc[ sz, spinz[ f[0] ] ];

 ss = Expand[ox + oy + oz];
 Hk = Jkondo ss;
];

H = H0 + Hk;

MAKESPINKET = SPIN;

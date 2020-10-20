def2ch[0];

SPIN = ToExpression @ param["spin", "extra"];

Module[{sx, sy, sz, ox, oy, oz, ss},
 sx = spinketbraX[SPIN];
 sy = spinketbraY[SPIN];
 sz = spinketbraZ[SPIN];

 o1x = nc[ sx, spinx[ f[0] ] ];
 o1y = nc[ sy, spiny[ f[0] ] ];
 o1z = nc[ sz, spinz[ f[0] ] ];

 o2x = nc[ sx, spinx[ f[1] ] ];
 o2y = nc[ sy, spiny[ f[1] ] ];
 o2z = nc[ sz, spinz[ f[1] ] ];

 ss1 = Expand[o1x + o1y + o1z];
 ss2 = Expand[o2x + o2y + o2z];
 Hk = Jkondo1 ss1 + Jkondo2 ss2;
];

H = H0 + Hk;

MAKESPINKET = SPIN;

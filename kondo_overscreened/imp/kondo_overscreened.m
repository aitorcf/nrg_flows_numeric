def2ch[1];

Hc = Jkondo1 spinspin[ f[0] , d[] ] + Jkondo2 spinspin[ f[1] , d[] ];
H1 = 0;
H = H1 + Hc;

BASISRULE = "projector1[ d[] ]";
nnop[ d[] ] = -1;
lrchain = { f[0] , d[] , f[1] };

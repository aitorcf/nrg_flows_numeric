def2ch[2];

Hc = gammaPol hop[ f[0] , d[] ] + gammaPol hop[ f[0] , a[] ] + gammaPol hop[ f[1] , d[] ] + gammaPol hop[ f[1] , a[] ];
Ha = U pow[ number[a[]] - 1, 2 ];
Hd = U pow[ number[d[]] - 1, 2 ];

H = Hc + Ha + Hd;

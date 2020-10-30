def2ch[2];

Hc = gammaPolch1 hop[ f[0] , d[] ] + gammaPolch1 hop[ f[0] , a[] ] + gammaPolch2 hop[ f[1] , d[] ] + gammaPolch2 hop[ f[1] , a[] ];
Ha = U pow[ number[a[]] - 1, 2 ];
Hd = U pow[ number[d[]] - 1, 2 ];

H = Hc + Ha + Hd;

Исходная тональность — мажор или минор. Пока будет только мажор, с минором разберемся чуть позже, принципиально ничего сложного там не будет.

Интервал задаётся парой (ступень_интервал). Например:
 * I_l3 — большая терция на первой ступени (large third).
 * VIb_e2 — увеличенная секунда на 6 пониженной ступени (extended second).
 * VII_r5 — уменьшенная квинта на 7 ступени (reduced fifth).

Интервалы могут иметь «флаги», т.е. какие-то свойства, пока пусть будут такие:
 * T — интервал из тонического трезвучия.
 * D — интервал «доминантового» типа (есть VII ступень).
 * H — в интервале есть гармоническая (для мажора VIb ступень).
 * A — наличие иных альтераций, например IIb.

Матрица переходов задаётся через ->
```
I_l3->II_s3
II_s3->I_l3
II_s3->III_s3
III_s3->II_s2
III_s3->III_p5
III_p5->III_s6
...
```

Лог ученика — вся цепочка, знаком ! помечается интервал или ступень, если была допущена ошибка. Одна строка — одно задание, если нет знака ! — всё разгадано было правильно. Все цепочки — в хронологическом порядке, как они давались учащемуся, т.е. можно пользоваться этим, чтобы понимать, что какую-то ошибку учащийся перестал делать, а через какое-то время перепроверить ещё раз.

```
2021-02-26_02:42 I_l3->II_s3->VII_r5->I_l3
2021-02-26_02:52 III_s3->III_!p5->II_l6->I_p8
```




#include <stdio.h>

int main()
{
int x,sum,average,T_0,T_1,T_2;
L_0: //(begin_block, whileProg, _, _)
L_1:scanf("%d",&x); //(inp, x, _, _)
L_2:sum=0; //(:=, 0, _, sum)
L_3:count=0; //(:=, 0, _, count)
L_4:if(x > 1) goto L_6; //(>, x, 1, 6)
L_5:goto L_11; //(jump, _, _, 11)
L_6:T_0=sum+x; //(+, sum, x, T_0)
L_7:sum=T_0; //(:=, T_0, _, sum)
L_8:T_1=count+1; //(+, count, 1, T_1)
L_9:count=T_1; //(:=, T_1, _, count)
L_10:goto L_4; //(jump, _, _, 4)
L_11:T_2=sum/count; //(/, sum, count, T_2)
L_12:average=T_2; //(:=, T_2, _, average)
L_13:printf("%d",average); //(out, average, _, _)
L_14:{}
L_15: //(end_block, whileProg, _, _)
}
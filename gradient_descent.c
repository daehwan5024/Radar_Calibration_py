#include <stdio.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <string.h>

int main() {
    int num_radar = 6;
    double posCalibrated[3][6] =  {
        {15.77746109, 15.23650632,  0.        , 21.14411717, 13.91277049,
         1.73082837},
        { -0.27104993,  0.60431148,  0.        ,  0.        , 14.53701127,
         7.60654262},
        {-3.00694904, -3.05630083,  0.        ,  0.        ,  0.        ,
        0.87310546}
    };
    double distance[6][6] = {
        {0.        ,  1.        , 16.06373211,  6.15761382, 15.22489705,
        16.51000616},
        {1.        ,  0.        , 15.5517617 ,  6.67877482, 14.3252705 ,
        15.72147447},
        {16.06373211, 15.5517617 ,  0.        , 21.14411717, 20.12187564,
         7.84968602},
        {6.15761382,  6.67877482, 21.14411717,  0.        , 16.23628872,
        20.86857891},
        {15.22489705, 14.3252705 , 20.12187564, 16.23628872,  0.        ,
        14.04255755},
        {16.51000616, 15.72147447,  7.84968602, 20.86857891, 14.04255755,
         0.        },
    };
    int grad = 0;

    struct timeval  tv1, tv2;
    gettimeofday(&tv1, NULL);
    while(grad++<500000){
        double loss[3][num_radar];
        memset(loss, 0, 3*num_radar*sizeof(double));
        for(int i=0;i<8;i++) {
            double loss_t[3] = {0};
            for(int j=0;j<num_radar;j++) {
                if(i==j) continue;
                double diff[3] = {posCalibrated[0][i] - posCalibrated[0][j], posCalibrated[1][i] - posCalibrated[1][j],
                                posCalibrated[2][i] - posCalibrated[2][j]};
                double dist_ij = sqrt(diff[0]*diff[0] + diff[1]*diff[1] + diff[2]*diff[2]);
                double constant = (dist_ij - distance[i][j])/dist_ij;
                loss_t[0] += 2*constant*diff[0];
                loss_t[1] += 2*constant*diff[1];
                loss_t[2] += 2*constant*diff[2];
            }
            loss[0][i] = loss_t[0]; loss[1][i] = loss_t[1]; loss[2][i] = loss_t[2];
        }
        for(int ii=0;ii<3;ii++) {
            for(int jj=0;jj<num_radar;jj++) {
                posCalibrated[ii][jj] -= loss[ii][jj]*0.0005;
            }
        }
    }
    gettimeofday(&tv2, NULL);
    printf ("Total time = %f seconds\n",
         (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
         (double) (tv2.tv_sec - tv1.tv_sec));
    for(int ii=0;ii<3;ii++) {
        for(int jj=0;jj<num_radar;jj++) {
            printf("%8f ", posCalibrated[ii][jj]);
        }
        printf("\n");
    }
}
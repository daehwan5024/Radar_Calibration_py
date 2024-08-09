#include <math.h>
#include <string.h>
#include <stdbool.h>

void gradient(int num_radar, bool *isnan_1D, double *posCalibrated_1D, double *distance_1D) {
    int grad = 0;
    double loss[3][num_radar];
    double posCalibrated[3][num_radar];
    bool isnan[num_radar][num_radar];
    double distance[num_radar][num_radar];
    for(int i=0;i<3;i++) {
        for(int j=0;j<num_radar;j++) {
            posCalibrated[i][j] = posCalibrated_1D[i*num_radar + j];
        }
    }
    for(int i=0;i<num_radar;i++) {
        for(int j=0;j<num_radar;j++) {
            distance[i][j] = distance_1D[i*num_radar + j];
            isnan[i][j] = isnan_1D[i*num_radar + j];
        }
    }
    // Need to verify iteration number and step size
    // Currently using large iteration number and small step size
    while(grad++<500000){
        memset(loss, 0, 3*num_radar*sizeof(double));
        for(int i=0;i<num_radar;i++) {
            double loss_t[3] = {0};
            for(int j=0;j<num_radar;j++) {
                if(i==j) continue;
                if(isnan[i][j]) continue;
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
    for(int i=0;i<3;i++) {
        for(int j=0;j<num_radar;j++) {
            posCalibrated_1D[i*num_radar+j] = posCalibrated[i][j];
        }
    }
}
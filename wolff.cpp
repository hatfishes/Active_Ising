#include <cmath>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iostream>
#include <math.h>
#include <sstream>
#include <stdlib.h>
#include <string>
#include <time.h>
#include <vector>
#include <queue>
using namespace std;

int SAMPLE_INT = 5000;
int REGULAR_INT = 100;
double T = 2;
int step = 0;
double beta_ = 1.0 / T;
int totalstep = 5000000;
string filename = "";

double acc;
double acc_rate;

double h = 0;   // external field
double J = 1.0; //
int Lx = 100;
int Ly = 1;

double E = 0;
double M = 0;
double k = 1 / double(Lx);

struct Spin {
  int value;
  bool inCluster;  // Added to track whether the spin is in the cluster
};

vector<vector<Spin>> spins(Lx, vector<Spin>(Ly));

void mc_step();
void sample();
void regulate();
double Hamiltonian();
void init();
void end();
int randSpin();
double totEnerg();
string getconfig();
void clusterFlip(int i, int j);

void addNeighborsToCluster(queue<pair<int, int>>& cluster, int i, int j) {
  // Add neighboring spins to the cluster
  cluster.push(make_pair((i + 1) % Lx, j));
  cluster.push(make_pair((i - 1 + Lx) % Lx, j));
}

void clusterFlip(int i, int j) {
  // Perform cluster flip using the Wolff algorithm
  queue<pair<int, int>> cluster;
  cluster.push(make_pair(i, j));
  spins[i][j].inCluster = true;
  int clusterSize = 1;

  while (!cluster.empty()) {
    pair<int, int> currentSpin = cluster.front();
    cluster.pop();

    int x = currentSpin.first;
    int y = currentSpin.second;

    // Check neighboring spins and add them to the cluster with a probability
    if (!spins[(x + 1) % Lx][y].inCluster && spins[(x + 1) % Lx][y].value == spins[x][y].value && exp(-beta_) > rand() / double(RAND_MAX)) {
      cluster.push(make_pair((x + 1) % Lx, y));
      spins[(x + 1) % Lx][y].inCluster = true;
      clusterSize++;
    }

    if (!spins[(x - 1 + Lx) % Lx][y].inCluster && spins[(x - 1 + Lx) % Lx][y].value == spins[x][y].value && exp(-beta_) > rand() / double(RAND_MAX)) {
      cluster.push(make_pair((x - 1 + Lx) % Lx, y));
      spins[(x - 1 + Lx) % Lx][y].inCluster = true;
      clusterSize++;
    }
  }

  // Flip spins in the cluster
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      if (spins[i][j].inCluster) {
        spins[i][j].value = -spins[i][j].value;
        M += 2 * spins[i][j].value;
      }
      spins[i][j].inCluster = false;  // Reset inCluster flag
    }
  }
}



// Rest of the code remains unchanged

int randSpin() { return (rand() % 2) == 0 ? 1 : -1; }

double totEnerg(const vector<vector<Spin>> &spins) {
  double energy = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      energy += -J * spins[i][j].value *
                spins[(i + 1) % Lx][j].value + h * spins[i][j].value;
    }
  }

  return energy;
}

double totMagne(const vector<vector<Spin>> &spins) {
  double magne = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      magne += spins[i][j].value;
    }
  }
  return magne;
}

string getconfig(){
  string config = "";
  for(int j=0 ; j < Ly ; j++){
    for(int i=0 ; i < Lx ; i++ ){
      if(spins[i][j].value == -1){
        config += "-";
      }else{
        config += "+";
      }
    }
    config += "&";
  }
  return config;
}

void sample() {

  acc_rate = acc / double(SAMPLE_INT);
  
  E = totEnerg(spins);
  M = totMagne(spins);

  string config = getconfig();

  ofstream oa(filename, ios::app);
  oa << step << " " << E << " " << M << " " << acc_rate <<" " << h << " " << config <<endl;

  acc = 0;

  // n = totalstep / SAMPLE_INT;
  // T -= 10.0 / double (n) ;
  // beta_ = 1.0 / T;
  oa.close();
}

void regulate(){
 // J = -0.3* k *abs(M) +1;
 // h =- 0.1 * k * abs(M) ;
}

void init() {
  srand(unsigned(time(0)));

  cout << "T: " << T << endl;

  // generate a random configuration

  step = 0;

  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      spins[i][j].value = randSpin();
    }
  }
  E = totEnerg(spins);
  M = totMagne(spins);
  cout << "initialized" << endl;
}

void mc_step() {
  int i = rand() % Lx;
  int j = rand() % Ly;

  // Perform cluster flip
  clusterFlip(i, j);

  // Update energy and magnetization
  E = totEnerg(spins);
}

int main(int argc, char *argv[]) {

  cout << argv[0] << endl;
  T = atof(argv[1]);
  beta_ = 1.0 / T;

  // 生成文件名
  ostringstream oss;
  oss << "data/" << T  ;
  filename = oss.str();
cout << filename << endl;

  init();

  ofstream oa(filename);
  //这里写data文件的第一行，也就是每列数据的标题。
  oa << "step"
     << " "
     << "Energy"
     << " "
     << "Magnet"
     << " "
     << "acc" 
     << " "
     << "h"
     << " "
     << "config"
     << endl;

  for (int i = 0; i < totalstep; i++) {
    mc_step();
    step++;
    if (step % SAMPLE_INT == 1) {
      sample();
    }
    if(step % REGULAR_INT == 1){
      regulate();
    }
  }
  // end();
  oa.close();

  cout << "simulation completed" << endl;
  return 0;
}

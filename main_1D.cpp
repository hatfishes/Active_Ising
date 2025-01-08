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
using namespace ::std;

int SAMPLE_INT = 5000;
double T = 2;
int step = 0;
double beta_ = 1.0 / T;
int totalstep = 50000000;
string filename = "";

double acc;
double acc_rate;

double h = 0;   // external field
double J = 1.0; //
int Lx = 20;
int Ly = 1;
struct Spin {
  int value;
};

vector<vector<Spin>> spins(Lx, vector<Spin>(Ly));

void mc_step();
void sample();
double Hamiltonian();
void init();
void end();
int randSpin();
double totEnerg();
string getconfig();

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

  cout << "initialized" << endl;
}

void mc_step() {
  int i = rand() % Lx;
  int j = rand() % Ly;

  //   cout << step <<  ": "  << i << "," << j<<endl;
// 计算的是当前格点的能量的负值，乘上两倍。 表示的是翻转前后的差值
//也就是说，当前格点的能量若是大于零，则dE<=0 ,则直接接受；反之以一定概率接受。
  double dE =
      2 * J * spins[i][j].value *
      (spins[(i + 1) % Lx][j].value + spins[(i - 1 + Lx) % Lx][j].value );

  if (dE <= 0 || exp(-beta_ * dE) > rand() / double(RAND_MAX)) {
    spins[i][j].value = -spins[i][j].value;
    acc++;
    //   cout << "flip:" <<  i << "," << j <<endl;
  }
}

int randSpin() { return (rand() % 2) == 0 ? 1 : -1; }

double totEnerg(const vector<vector<Spin>> &spins) {
  double energy = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      energy += -J * spins[i][j].value *
                spins[(i + 1) % Lx][j].value ;
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
  double E = totEnerg(spins);
  double M = totMagne(spins);
  acc_rate = acc / double(SAMPLE_INT);
  
  string config = getconfig();
  
  ofstream oa(filename, ios::app);
  oa << step << " " << E << " " << M << " " << acc_rate << endl;

  acc = 0;

  // n = totalstep / SAMPLE_INT;
  // T -= 10.0 / double (n) ;
  // beta_ = 1.0 / T;
  oa.close();
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
  oa << "step"
     << " "
     << "Energy"
     << " "
     << "Magnet"
     << " "
     << "acc" << endl;
  for (int i = 0; i < totalstep; i++) {
    mc_step();
    step++;
    if (step % SAMPLE_INT == 1) {
      sample();
    }
  }
  // end();
  oa.close();

  cout << "simulation complete123d" << endl;
  return 0;
}

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

int SAMPLE_INT = 50000;
int REGULATION_INT = 100;
double T = 2;
int step = 0;
double beta_ = 1.0 / T;
int totalstep = 500000000;
string filename = "";

double acc;
double acc_rate;

double h = 0;   // external field
double J = 1.0; //
int Lx = 32;
int Ly = 32;
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
double getEnerg();
double getMagne();
string getconfig();
void regulate();

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

  double dE =
      2 * J * spins[i][j].value *
      (spins[(i + 1) % Lx][j].value + spins[(i - 1 + Lx) % Lx][j].value +
       spins[i][(j + 1) % Ly].value + spins[i][(j - 1 + Ly) % Ly].value);

  if (dE <= 0 || exp(-beta_ * dE) > rand() / double(RAND_MAX)) {
    spins[i][j].value = -spins[i][j].value;
    acc++;
    //   cout << "flip:" <<  i << "," << j <<endl;
  }
}

int randSpin() { return (rand() % 2) == 0 ? 1 : -1; }

double getEnerg(const vector<vector<Spin>> &spins) {
  double energy = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      energy += -J * spins[i][j].value *
                (spins[(i + 1) % Lx][j].value + spins[i][(j + 1) % Ly].value);
    }
  }

  return energy /Lx / Ly;
}

double getMagne(const vector<vector<Spin>> &spins) {
  double magne = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      magne += spins[i][j].value;
    }
  }
  return magne /Lx /Ly;
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
  double E = getEnerg(spins);
  double M = getMagne(spins);

  acc_rate = acc / double(SAMPLE_INT);

  string config = getconfig();
  ofstream oa(filename, ios::app);
  oa << step << " " << E << " " << M << " " << acc_rate <<" "<< J  << " "<< config << endl;

  acc = 0;

  // n = totalstep / SAMPLE_INT;
  // T -= 10.0 / double (n) ;
  // beta_ = 1.0 / T;
  oa.close();
}

void regulate(){
  double m = getMagne(spins);
  J = -0.2* (m-0.3) +1 ;
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
     << "acc" 
     <<" "
     <<"J"
     <<" "
     <<"config"
     << endl;
  for (int i = 0; i < totalstep; i++) {
    mc_step();
    step++;
    if (step % SAMPLE_INT == 1) {
      sample();
    }
    if (step % REGULATION_INT == 1) {
      regulate();
    }
  }
  // end();
  oa.close();

  cout << "simulation completedasdasd" << endl;
  return 0;
}

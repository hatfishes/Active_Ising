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

int SAMPLE_INT = 10000000;

double T = 2;
double dT = 0.1/1000;
long long step = 0;
double beta_ = 1.0 / T;
long long totalstep = 100000000000;
string filename = "";
string configfilename = "";

double acc;
double acc_rate;

double h = 0;   // external field
double dh = 1/double(1000);
double J = 1.0; //
double k= 0.2; //regulation coefficient

int Lx = 10000;
int Ly = 1;
//int REGULAR_INT = Ly * Lx;
int REGULAR_INT = 1;


double E = 0;
double M = 0;
//double k = 1 / double(Lx);

struct Spin {
  int value;
};

vector<vector<Spin>> spins(Lx, vector<Spin>(Ly));

void mc_step();
void sample();
void regulate();
double Hamiltonian();
void init();
void end();
int randSpin();
double getEnerg();
double getMagne();
string getconfig();

void mc_step() {
  int i = rand() % Lx;
  int j = rand() % Ly;
  double dM = -2*spins[i][j].value;
  //   cout << step <<  ": "  << i << "," << j<<endl;
 // 计算的是当前格点的能量的负值，乘上两倍。 表示的是翻转前后的差值
 //也就是说，当前格点的能量若是大于零，则dE<=0 ,则直接接受；反之以一定概率接受。
  double dE =
      2 * J * spins[i][j].value *
      (spins[(i + 1) % Lx][j].value + spins[(i - 1 + Lx) % Lx][j].value ) - 2*h * spins[i][j].value ;
  //增加一个判断，考察J的变化对于能量的影响
 // if(M * spins[i][j].value >= 0 ){
 //    dE -= 2*k  / J *E;
 //  }else{
 //    dE += 2*k  / J *E;
 //  }

  // dE += k*(abs(M+dM/double(Lx))-abs(M)) *Lx  / J *E;
   dE += k*((M+dM/double(Lx))*(M+dM/double(Lx))- M*M ) *E *Lx/J;


  if (dE <= 0 || exp(-beta_ * dE) > rand() / double(RAND_MAX)) {
    spins[i][j].value = -spins[i][j].value;
    acc++;
    //   cout << "flip:" <<  i << "," << j <<endl;
    M += dM/double(Lx);
    //2 * double(spins[i][j].value) /double( Lx); //注意这里因为上面已经翻转过了，所以是加的新的自旋。
    E += dE/ Lx;                                               //
  }
}

int randSpin() { return (rand() % 2) == 0 ? 1 : -1; }

double getEnerg(const vector<vector<Spin>> &spins) {
  double energy = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      energy += -J * spins[i][j].value *
          spins[(i + 1) % Lx][j].value + h * spins[i][j].value;
    }
  }

  return energy/Lx/Ly;
}

double getMagne(const vector<vector<Spin>> &spins) {
  double magne = 0.0;
  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      magne += spins[i][j].value;
    }
  }
  return double(magne)/ double(Lx)/double(Ly);
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
    //config += "&";
  }
  return config;
}

void sample(std::ofstream& oa, std::ofstream& ob) {

  acc_rate = acc / double(SAMPLE_INT);
  
  E = getEnerg(spins);
  //M = getMagne(spins);

  //string config = getconfig();
  //h += dh    ;
  //ofstream oa(filename, ios::app);
  oa << step << "," << E << "," << M << "," << acc_rate << "," << J << endl;
  //ob << config << endl;
  acc = 0;

  // n = totalstep / SAMPLE_INT;
  // T -= 10.0 / double (n) ;
  // beta_ = 1.0 / T;
  //oa.close();
}


//调整相互作用强度
void regulate(){
  //M = getMagne(spins);
  J = k * M * M +1;
  //h =  0.05  * M ;
}

void init() {
  srand(unsigned(time(0)));
  cout << "T: " << T <<",k:"<<k <<",Lx:"<<Lx << endl;
  // generate a random configuration
  step = 0;

  for (int i = 0; i < Lx; i++) {
    for (int j = 0; j < Ly; j++) {
      spins[i][j].value = randSpin();
     // spins[i][j].value = 1;
    }
  }

  E = getEnerg(spins);
  M = getMagne(spins);
  cout << "initialized" << endl;
}


int main(int argc, char *argv[]) {

  cout << argv[0] << endl;
  T = atof(argv[1]);
  beta_ = 1.0 / T;

  // 生成文件名，使用的是专门用来拼接字符串的类
  ostringstream oss;
  oss << "data/k" << k << "L" << Lx << "T" << T <<".csv";
  filename = oss.str();
  cout << filename << endl;

  ostringstream oss2;
  oss2 << "configs/k" << k << "L" << Lx << "T" << T <<".csv";
  configfilename = oss2.str();
  cout << configfilename << endl;

  init();

  ofstream oa(filename);
  //这里写data文件的第一行，也就是每列数据的标题。
  oa << "step,"
     << "Energy,"
     << "Magnet,"
     << "acc," 
     << "J"
     << endl;
  
  ofstream ob(configfilename);
  ob << "config," << endl;
  step = 0;
  while(step < totalstep) {
    mc_step();
    regulate();
    step++;
    if (step % SAMPLE_INT == 1) {
      sample(oa,ob);
    }
    //if(step % REGULAR_INT == 1){
    //regulate();
    //}
  }
  // end();
  oa.close();
  ob.close();

  cout << "simulation completed" << endl;
  return 0;
}


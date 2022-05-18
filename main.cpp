
 
#include "../source/MoorDyn2.h" 
#include <stdexcept>
#include <iostream>
//#include <algorithm>


using namespace std;


int main(int argc, char* argv[])
{
    MoorDyn system = MoorDyn_Create(argv[1]);
    if (!system)
    {
        cerr << "Failure Creating the Mooring system" << endl;
        return 1;
    }

    const unsigned int n_dof = MoorDyn_NCoupledDOF(system);
    if (n_dof){
        cerr << "No coupled Degrees Of Freedom were expected, but " << n_dof
             << "were reported" << endl;
        MoorDyn_Close(system);
        return 2;
    }

    int err;
    err = MoorDyn_Init(system, NULL, NULL);
    if (err != MOORDYN_SUCCESS){
        cerr << "Failure during the mooring initialization: " << err << endl;
        MoorDyn_Close(system);
        return 3;
    }

    
    double dt = 0.00016;
    const unsigned int nts = 100000;
    //double dt = 0.001;
    //const unsigned int nts = 1000;
    for (unsigned int i = 0; i < nts; i++){
        double t = i * dt;

        err = MoorDyn_Step(system, NULL, NULL, NULL, &t, &dt);
        if (err != MOORDYN_SUCCESS) {
            cerr << "Failure during the mooring step " << i << ": "
                << err << endl;
            MoorDyn_Close(system);
            return 4;
        }
    }

    err = MoorDyn_Close(system);
    
    return 0;
}

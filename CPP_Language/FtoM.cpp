#include <iostream>
using namespace std;

/*
 * Proyecto 1-1
 * Conversor de pies a metros.
 *
 * */

int main(){
    double feet;
    double meters;

    cout << "Ingrese la longitud en pies: ";
    cin >> feet;

    meters = feet / 3.28; //1 metro = 3.28 pies

    cout << feet << " pies es equivalente a " << meters << " metros." << "\n";

    return 0;
    }



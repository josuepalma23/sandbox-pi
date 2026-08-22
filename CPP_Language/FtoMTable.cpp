#include <iostream>
using namespace std;

/*
 * Proyecto 1-2
 * Programa de una tabla de conversion de pies a metros.
 *
 * */

int main(){
    double pies;
    double metros;
    int contador = 0;

    for(pies = 1.0; pies <= 100.0; pies++){
        metros = pies / 3.28;
        cout << pies << " pies equivale a " << metros << " metros." << "\n";
        
        contador++;

        if(contador == 10){
            cout << "\n";
            contador = 0;
            }
        }
    return 0;
    }   

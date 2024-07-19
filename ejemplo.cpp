// Un vendedor recibe un sueldo base mas un 10% extra por comision de sus ventas, el vendedor desea saber cuando dinero obtendra por concepto de comiciones por las tres ventas que realiza en el mes y el total que recibira en el mes tomando en cuenta su sueldo base y comisiones.

#include <iostream>
using namespace std;

int main()
{
    float sueldo, venta1, venta2, venta3, comision, total;
    cout << "Ingrese su sueldo base: ";
    cin >> sueldo;
    cout << "Ingrese el valor de la primera venta: ";
    cin >> venta1;
    cout << "Ingrese el valor de la segunda venta: ";
    cin >> venta2;
    cout << "Ingrese el valor de la tercera venta: ";
    cin >> venta3;
    comision = (venta1 + venta2 + venta3) * 0.1;
    total = sueldo + comision;
    cout << "El total a recibir es: " << total << endl;
    return 0;
}

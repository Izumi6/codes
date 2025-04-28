#include <iostream>
using namespace std;

int main()
{
    int n;
    string city[20];
    int matrix[50][50];
    cout << "Enter no. of cities: ";
    cin >> n;
    for(int i=0; i<n; i++)
    {
        cout << "Enter name of city"<< i+1 ;
        cin >> city[i];
    }
    for(int i=0; i<n; i++){
        for(int j=i+1; j<n; j++)
        {
            cout << "Enter time required from city" << city[i] <<"to the city" << city[j]<< endl;
            cin >> matrix[i][j];
            matrix[j][i]=matrix[i][j];
        }
    }
    for(int i=0; i<n; i++)
    {
        cout << "\t" << city[i] << "\t";
    }
    for(int i=0; i<n; i++)
    {
        cout << "\n"<< city[i];
        for(int j=0; j<n; j++)
        {
            cout << "\t" << matrix[i][j] << "\t";
        }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KafelekPlatformy : MonoBehaviour
{
    public Transform punktStartowy;     // Punkt poczatkowy naszego kafelka -> miejsce polaczenia z poprzednim kafelkiem
    public Transform punktKoncowy;      // Punkt koncowy naszego kafelka -> miejsce polaczenia z nastepnym kafelkiem
    public GameObject[] przeszkody;     // Rozne typy naszych przeszkod ktore zdefinujemy  -> losowo aktywowane

    public void AktywujLosowaPrzeszkode()        //Metoda aktywujaca losowa przeszkode 
    {
        DezaktywujWszystkiePrzeszkody();
        System.Random los = new System.Random();
        int indeks = los.Next(0, przeszkody.Length);
        przeszkody[indeks].SetActive(true);
    }

    public void DezaktywujWszystkiePrzeszkody()   //Metoda deaktywujaca wszystkie przeszkody
    {
        for (int i = 0; i < przeszkody.Length; i++)
        {
            przeszkody[i].SetActive(false);
        }
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KafelekPlatformy : MonoBehaviour
{
    public Transform punktStartowy;     // Punkt poczatkowy naszego kafelka -> miejsce polaczenia z poprzednim kafelkiem
    public Transform punktKoncowy;      // Punkt koncowy naszego kafelka -> miejsce polaczenia z nastepnym kafelkiem
    public GameObject[] przeszkody;     // Rozne typy naszych przeszkod ktore zdefinujemy  -> losowo aktywowane
    public bool aktywujPrzeszkody = false;

    public void AktywujLosowaPrzeszkode()        //Metoda aktywujaca losowa przeszkode 
    {
        DezaktywujWszystkiePrzeszkody();
        if (!aktywujPrzeszkody || przeszkody == null || przeszkody.Length == 0)
        {
            return;
        }

        int indeks = Random.Range(0, przeszkody.Length);
        if (przeszkody[indeks] != null)
        {
            przeszkody[indeks].SetActive(true);
        }
    }

    public void DezaktywujWszystkiePrzeszkody()   //Metoda deaktywujaca wszystkie przeszkody
    {
        if (przeszkody == null)
        {
            return;
        }

        for (int i = 0; i < przeszkody.Length; i++)
        {
            if (przeszkody[i] != null)
            {
                przeszkody[i].SetActive(false);
            }
        }
    }
}

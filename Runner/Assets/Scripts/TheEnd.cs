using TMPro;
using UnityEngine;

public class TheEnd : MonoBehaviour
{
    private int wynikKoncowy;
    public TextMeshProUGUI wynikTextMesh;

    void Start()
    {
        wynikKoncowy = PlayerPrefs.GetInt("Wynik gry", 0); // 0 to wartosc domyslna jesli nic nie zapisano
        wynikTextMesh.text = "Twoj wynik koncowy: " + wynikKoncowy;
    }

    // void OnGUI()
    // {
    //     GUI.skin.label.fontSize = 24; 
    //     GUI.color = Color.red;
    //     GUI.Label(new Rect(Screen.width / 2 - 100, Screen.height / 2 - 50, 300, 100), "Twoj wynik koncowy: " + wynikKoncowy);
    // }
}

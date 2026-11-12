using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class SManager : MonoBehaviour
{
   public void IdzDoSceny()
    {
        
        SceneManager.LoadScene (1);
    }
    
    public void Wyjdz()
    {
        Debug.Log("Wyjście z gry");
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }

    public void IdzInstrukca()

    {
         SceneManager.LoadScene (2);  
    }

     public void IdzMenu()

    {
         SceneManager.LoadScene (0);  
    }

}

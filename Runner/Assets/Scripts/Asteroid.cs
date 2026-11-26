using UnityEngine;

public class Asteroid : MonoBehaviour
{
    void OnCollisionEnter(Collision collision)
    {
        Gracz gracz = collision.gameObject.GetComponentInParent<Gracz>();
        if (gracz != null)
        {
            if (!gracz.IsShieldActive && GeneratorPodloza.instancja != null)
            {
                GeneratorPodloza.instancja.graSkonczona = true;
            }
            Destroy(gameObject);
            return;
        }

        if (collision.gameObject.CompareTag("Floor"))
        {
            Destroy(gameObject);
        }
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Shield"))
        {
            Destroy(gameObject);
        }
    }
}

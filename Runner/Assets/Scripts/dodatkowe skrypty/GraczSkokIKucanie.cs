using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class GraczSkokIKucanie : MonoBehaviour
{
    public float grawitacja = -20f;
    public float wysokoscSkoku = 2.8f;
    public float predkoscRuchu = 4f;

    Rigidbody rigidbodyGracza;
    bool naZiemi = false;
    Vector3 domyslnaSkala;
    bool kuca = false;

    void Start()
    {
        rigidbodyGracza = GetComponent<Rigidbody>();
        rigidbodyGracza.constraints = RigidbodyConstraints.FreezeRotation;
        rigidbodyGracza.useGravity = false;
        domyslnaSkala = transform.localScale;
    }

    void Update()
    {
     
        float ruchPoziomy = Input.GetAxis("Horizontal");                       //ruch naszego gracza w poziomie
        Vector3 predkosc = rigidbodyGracza.linearVelocity;
        predkosc.x = ruchPoziomy * predkoscRuchu;
        rigidbodyGracza.linearVelocity = new Vector3(predkosc.x, rigidbodyGracza.linearVelocity.y, 0);

            
        if (Input.GetKeyDown(KeyCode.W) && naZiemi)                         //skok naszego gracza
        {
            rigidbodyGracza.linearVelocity = new Vector3(
                rigidbodyGracza.linearVelocity.x,
                ObliczPredkoscSkoku(),
                rigidbodyGracza.linearVelocity.z
            );
        }

        kuca = Input.GetKey(KeyCode.S);                                 //"kucanie" naszego gracza - proste skalowanie obiektu
        if (kuca)
        {
            transform.localScale = Vector3.Lerp(
                transform.localScale,
                new Vector3(domyslnaSkala.x, domyslnaSkala.y * 0.4f, domyslnaSkala.z),
                Time.deltaTime * 7
            );
        }
        else
        {
            transform.localScale = Vector3.Lerp(
                transform.localScale,
                domyslnaSkala,
                Time.deltaTime * 7
            );
        }
    }

    void FixedUpdate()
    {
       
        rigidbodyGracza.AddForce(new Vector3(0, -grawitacja * rigidbodyGracza.mass, 0));  //sztuczna grawitacja dla lepszej grywalnosci
        naZiemi = false;
    }

    void OnCollisionStay()
    {
        naZiemi = true;
    }

    float ObliczPredkoscSkoku()
    {
        return Mathf.Sqrt(2 * wysokoscSkoku * grawitacja);
    }

    void OnCollisionEnter(Collision kolizja)
    {
        if (kolizja.gameObject.tag == "Finish")
        {
            GeneratorPodloza.instancja.graSkonczona = true;
        }
    }
}

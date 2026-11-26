using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Gracz : MonoBehaviour
{
    public float grawitacja = 20f;
    public float wysokoscSkoku = 2.8f;
    public float predkoscRuchu = 4f;

    [Header("Shield")]
    public GameObject shieldObject;
    public KeyCode shieldKey = KeyCode.R;
    public float shieldDuration = 3f;
    public float shieldCooldown = 5f;

    public bool IsShieldActive => shieldActive;
    public float ShieldTimeRemaining => shieldActive ? Mathf.Max(0f, shieldTimer) : 0f;
    public float ShieldCooldownRemaining => Mathf.Max(0f, cooldownTimer);

    Rigidbody rigidbodyGracza;
    bool naZiemi = false;
    Vector3 domyslnaSkala;
    bool kuca = false;
    bool shieldActive = false;
    float shieldTimer = 0f;
    float cooldownTimer = 0f;

    void Start()
    {
        rigidbodyGracza = GetComponent<Rigidbody>();
        rigidbodyGracza.constraints = RigidbodyConstraints.FreezeRotation;
        rigidbodyGracza.useGravity = false; // uzywamy wlasnej grawitacji dla lepszej grywalnosci
        domyslnaSkala = transform.localScale;

        if (shieldObject == null)
        {
            Transform shieldTransform = transform.Find("Shield");
            if (shieldTransform != null)
            {
                shieldObject = shieldTransform.gameObject;
            }
        }

        if (shieldObject != null)
        {
            shieldObject.SetActive(false);
        }
    }

    void Update()
    {
        UpdateShield();

        float ruchPoziomy = Input.GetAxis("Horizontal");   
        float ruchPionowy = Input.GetAxis("Vertical");     

        float ruchGoraDol = 0f;                            
        if (Input.GetKey(KeyCode.Space)) ruchGoraDol = 1f; 
        if (Input.GetKey(KeyCode.LeftControl)) ruchGoraDol = -1f; 

        Vector3 predkosc = rigidbodyGracza.linearVelocity;
        predkosc.x = ruchPoziomy * predkoscRuchu;  
        predkosc.z = ruchPionowy * predkoscRuchu;  
        predkosc.y = ruchGoraDol * predkoscRuchu;  
        rigidbodyGracza.linearVelocity = predkosc;
    }

    void FixedUpdate()
    {
        // sztuczna grawitacja dziala tylko gdy NIE naciskamy spacji (lot naszym statkiem do gory)
        if (!Input.GetKey(KeyCode.Space))
        {
            rigidbodyGracza.AddForce(new Vector3(0, -grawitacja * rigidbodyGracza.mass, 0));
        }

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

    void UpdateShield()
    {
        if (shieldActive)
        {
            shieldTimer -= Time.deltaTime;
            if (shieldTimer <= 0f)
            {
                shieldActive = false;
                shieldTimer = 0f;
                if (shieldObject != null)
                {
                    shieldObject.SetActive(false);
                }
            }
        }
        else if (cooldownTimer > 0f)
        {
            cooldownTimer -= Time.deltaTime;
            if (cooldownTimer < 0f)
            {
                cooldownTimer = 0f;
            }
        }

        if (Input.GetKeyDown(shieldKey) && !shieldActive && cooldownTimer <= 0f && shieldObject != null)
        {
            shieldActive = true;
            shieldTimer = shieldDuration;
            cooldownTimer = shieldCooldown;
            shieldObject.SetActive(true);
        }
    }

    void OnCollisionEnter(Collision kolizja)
    {
        if (kolizja.gameObject.CompareTag("Finish") || kolizja.gameObject.GetComponent<Asteroid>() != null)
        {
            if (shieldActive)
            {
                Destroy(kolizja.gameObject);
                return;
            }

            if (GeneratorPodloza.instancja != null)
            {
                GeneratorPodloza.instancja.graSkonczona = true;
            }
        }
    }

    void OnTriggerEnter(Collider other)
    {
        if (shieldActive && (other.CompareTag("Finish") || other.GetComponent<Asteroid>() != null))
        {
            Destroy(other.gameObject);
        }
    }
}

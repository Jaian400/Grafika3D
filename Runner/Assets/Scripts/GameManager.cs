using TMPro;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    [Header("Asteroid spawning")]
    public GameObject asteroidPrefab;
    public Gracz gracz;
    public Transform asteroidSpawnPoint;
    public Vector2 spawnPointXOffsetRange = new Vector2(-5f, 5f);
    public float spawnHeight = 8f;
    public Vector2 distanceAheadRange = new Vector2(-0.5f, 0.75f);
    public float randomSideOffset = 0.5f;
    public Vector2 approachFromRightRange = new Vector2(8f, 14f);
    public Vector2 approachFromBehindRange = new Vector2(0f, 1.5f);
    public float spawnInterval = 3f;
    public float throwSpeed = 10f;
    public float asteroidLifetime = 30f;

    [Header("Difficulty")]
    public float difficultyRampDuration = 120f;
    public float difficultyExponent = 1.75f;
    public float minimumSpawnInterval = 1.25f;
    public float maximumThrowSpeed = 16f;
    public float maximumRandomSideOffset = 1.5f;

    [Header("Alert / Intensity Phases")]
    public TextMeshProUGUI alertTextMesh;
    public float phaseSwitchInterval = 20f;
    public string[] phaseLabels = { "ALERT: LEVEL 1", "ALERT: LEVEL 2", "ALERT: LEVEL 3" };
    public Color[] phaseColors = { Color.yellow, new Color(1f, 0.5f, 0f), Color.red };
    public float[] phaseSpawnRateMultipliers = { 1f, 1.35f, 1.75f };
    public float[] phaseSpeedMultipliers = { 1f, 1.2f, 1.45f };

    Collider playerCollider;
    Rigidbody playerRigidbody;
    float timeUntilNextSpawn;
    float elapsedPlayTime;
    int currentPhase = 1;

    void Start()
    {
        if (asteroidPrefab == null)
        {
            Debug.LogError("Assign an asteroid prefab to GameManager.", this);
            enabled = false;
            return;
        }

        if (asteroidPrefab.GetComponent<Rigidbody>() == null)
        {
            Debug.LogError("The asteroid prefab needs a Rigidbody component.", asteroidPrefab);
            enabled = false;
            return;
        }

        if (gracz == null)
        {
            gracz = FindFirstObjectByType<Gracz>();
        }

        if (gracz == null)
        {
            Debug.LogError("Assign the player (Gracz) to GameManager.", this);
            enabled = false;
            return;
        }

        playerRigidbody = gracz.GetComponent<Rigidbody>();
        if (playerRigidbody == null)
        {
            Debug.LogError("The player needs a Rigidbody component.", gracz);
            enabled = false;
            return;
        }

        playerCollider = gracz.GetComponentInChildren<Collider>();

        if (spawnInterval <= 0f || throwSpeed <= 0f || spawnHeight <= 0f ||
            randomSideOffset < 0f ||
            difficultyRampDuration <= 0f ||
            difficultyExponent <= 0f ||
            phaseSwitchInterval <= 0f ||
            minimumSpawnInterval <= 0f || minimumSpawnInterval > spawnInterval ||
            maximumThrowSpeed < throwSpeed ||
            maximumRandomSideOffset < randomSideOffset ||
            distanceAheadRange.y < distanceAheadRange.x ||
            !IsValidRange(approachFromRightRange) ||
            !IsValidRange(approachFromBehindRange))
        {
            Debug.LogError("Asteroid spawn and difficulty settings are invalid.", this);
            enabled = false;
            return;
        }

        timeUntilNextSpawn = spawnInterval;
        UpdateAlertUI();
    }

    void Update()
    {
        GeneratorPodloza generator = GeneratorPodloza.instancja;
        if (generator == null || !GeneratorPodloza.GraRozpoczeta || generator.graSkonczona)
        {
            return;
        }

        elapsedPlayTime += Time.deltaTime;
        int newPhase = Mathf.Clamp(Mathf.FloorToInt(elapsedPlayTime / phaseSwitchInterval) + 1, 1, 3);
        if (newPhase != currentPhase)
        {
            currentPhase = newPhase;
            UpdateAlertUI();
        }

        float linearProgress = Mathf.Clamp01(elapsedPlayTime / difficultyRampDuration);
        float difficulty = Mathf.Pow(linearProgress, difficultyExponent);
        timeUntilNextSpawn -= Time.deltaTime;
        if (timeUntilNextSpawn <= 0f)
        {
            SpawnAsteroid(difficulty);
            float spawnRateMultiplier = GetPhaseMultiplier(phaseSpawnRateMultipliers, currentPhase);
            timeUntilNextSpawn = Mathf.Lerp(spawnInterval, minimumSpawnInterval, difficulty) / spawnRateMultiplier;
        }
    }

    void SpawnAsteroid(float difficulty)
    {
        float speedMultiplier = GetPhaseMultiplier(phaseSpeedMultipliers, currentPhase);
        float currentThrowSpeed = Mathf.Lerp(throwSpeed, maximumThrowSpeed, difficulty) * speedMultiplier;
        Vector3 playerVelocity = Vector3.ProjectOnPlane(playerRigidbody.linearVelocity, Vector3.up);
        Vector3 forward = Vector3.ProjectOnPlane(gracz.transform.forward, Vector3.up).normalized;
        if (forward.sqrMagnitude < 0.001f)
        {
            forward = Vector3.forward;
        }

        Vector3 right = Vector3.ProjectOnPlane(gracz.transform.right, Vector3.up).normalized;
        if (right.sqrMagnitude < 0.001f)
        {
            right = Vector3.right;
        }

        float currentRandomSideOffset = Mathf.Lerp(randomSideOffset, maximumRandomSideOffset, difficulty);
        Vector3 aimOffset = forward * Random.Range(distanceAheadRange.x, distanceAheadRange.y)
            + right * Random.Range(-currentRandomSideOffset, currentRandomSideOffset);

        Vector3 spawnPosition = asteroidSpawnPoint != null
            ? asteroidSpawnPoint.position + Vector3.right * Random.Range(spawnPointXOffsetRange.x, spawnPointXOffsetRange.y)
            : gracz.transform.position + aimOffset
                + Vector3.up * spawnHeight
                + right * Random.Range(approachFromRightRange.x, approachFromRightRange.y)
                - forward * Random.Range(approachFromBehindRange.x, approachFromBehindRange.y);

        Vector3 playerCenter = playerCollider != null ? playerCollider.bounds.center : gracz.transform.position;
        float flightTime = Mathf.Max(0.2f, Vector3.Distance(spawnPosition, playerCenter) / currentThrowSpeed);
        Vector3 targetPosition = playerCenter + playerVelocity * flightTime + aimOffset;

        GameObject asteroid = Instantiate(asteroidPrefab, spawnPosition, asteroidPrefab.transform.rotation);
        Rigidbody asteroidRigidbody = asteroid.GetComponent<Rigidbody>();
        if (asteroidRigidbody == null)
        {
            Debug.LogError("The spawned asteroid has no Rigidbody component.", asteroid);
            Destroy(asteroid);
            return;
        }

        asteroidRigidbody.useGravity = false;
        asteroidRigidbody.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
        asteroidRigidbody.linearVelocity = (targetPosition - spawnPosition).normalized * currentThrowSpeed;

        if (asteroidLifetime > 0f)
        {
            Destroy(asteroid, asteroidLifetime);
        }
    }

    bool IsValidRange(Vector2 range)
    {
        return range.x >= 0f && range.y >= range.x;
    }

    void UpdateAlertUI()
    {
        if (alertTextMesh == null)
        {
            return;
        }

        int index = currentPhase - 1;
        alertTextMesh.text = (phaseLabels != null && index < phaseLabels.Length && !string.IsNullOrEmpty(phaseLabels[index]))
            ? phaseLabels[index]
            : "ALERT: LEVEL " + currentPhase;

        if (phaseColors != null && index < phaseColors.Length)
        {
            alertTextMesh.color = phaseColors[index];
        }
    }

    float GetPhaseMultiplier(float[] multipliers, int phase)
    {
        int index = phase - 1;
        if (multipliers != null && index >= 0 && index < multipliers.Length && multipliers[index] > 0f)
        {
            return multipliers[index];
        }

        return 1f;
    }
}
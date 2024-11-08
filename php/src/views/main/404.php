<script>
    let timeLeft = <?php echo $config::$time_before_redirect ?>;
    setInterval(() => {
        timeLeft -= 1;
        document.getElementById("time").textContent = timeLeft;
        if (timeLeft == 0) {
            window.location.href = "/";
        }
    }, 1000)
</script>
<div style="display:flex;flex-direction:column;justify-items:center;align-items:center;width:100%;height:100%;">
    <p>Vous vous êtes perdus ?</p>
    <p>Atterissage sur la page d'acceuil du site dans <span id="time"><?php echo $config::$time_before_redirect ?></span> secondes !</p>
</div>
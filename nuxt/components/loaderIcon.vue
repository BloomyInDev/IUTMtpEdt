<template>
    <div id="loader-container">
        <div class="loader" />
    </div>
</template>
<style>
#loader-container {
    display: grid;
    width: 96px;
    height: 96px;
    place-items: center;

}

.loader {
    width: 15px;
    height: 15px;
    aspect-ratio: 1;
    position: relative;
    animation: l9-0 1.25s infinite steps(2);
}
.loader::before,
.loader::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: #fff;
}
.loader::before {
    box-shadow: 26px 0;
    transform: translateX(-26px);
    animation: l9-1 0.625s infinite linear alternate;
}
.loader::after {
    transform: translateX(13px) rotate(0deg) translateX(13px);
    animation: l9-2 0.625s infinite linear alternate;
}
@keyframes l9-0 {
    0%,
    49.9% {
        transform: scale(1);
    }
    50%,
    100% {
        transform: scale(-1);
    }
}
@keyframes l9-1 {
    100% {
        box-shadow: 52px 0;
    }
}
@keyframes l9-2 {
    100% {
        transform: translateX(13px) rotate(-180deg) translateX(13px);
    }
}
</style>

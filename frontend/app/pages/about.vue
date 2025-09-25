<script setup lang="ts">
import auth from '~/middleware/auth';

definePageMeta({
  middleware: auth,
});
</script>

<template>
  <section>
    <p>This page will be displayed at the /about route.</p>
  </section>
</template>

<script setup lang="ts">
import redirectHome from '~/middleware/redirectHome';

definePageMeta({
  middleware: redirectHome,
});
</script>

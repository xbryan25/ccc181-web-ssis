<script setup lang="ts">
import { capitalizeWords } from "#imports";

const props = defineProps<{
  entityType: string;
}>();

console.log("imports " + props.entityType);
</script>

<template>
  <div class="flex gap-3">
    <IconField>
      <FloatLabel variant="on">
        <InputIcon>
          <Icon name="solar:magnifer-linear" />
        </InputIcon>
        <InputText id="over_label" />
        <label for="over_label">Search</label>
      </FloatLabel>
    </IconField>

    <Button>
      <Icon name="solar:filter-linear" class="h-6 w-6" />
      <p class="font-medium">Profile</p>
    </Button>

    <Button>
      <Icon name="solar:sort-linear" class="h-6 w-6" />
      <p class="font-medium">Sort Options</p>
    </Button>

    <Button class="w-44 ml-auto">
      <Icon name="solar:add-circle-linear" class="h-6 w-6" />
      <p class="font-medium">Add {{ props.entityType.slice(0, -1) }}</p>
    </Button>
  </div>
</template>

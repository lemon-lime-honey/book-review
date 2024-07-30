<script>
  export let error;
</script>

{#if typeof error.detail === 'string'}
  <div class="alert alert-warning" role="alert">
    {error.detail}
  </div>
{:else if typeof error.detail === 'object' && error.detail.length > 0}
  <div class="alert alert-warning" role="alert">
    {#each error.detail as err, i}
      <p class="mb-1"><strong>{err.loc[1]}</strong>: {err.msg}</p>
    {/each}
  </div>
{/if}

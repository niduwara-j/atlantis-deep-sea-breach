# Stage 2: Tide-Keeper Hijack - Progressive Hints

### Hint 1 (Cost: 10 points)
> Look closely at the **Support desk** navigation tab. Operator tickets frequently contain attached diagnostic reports or request captures from past incidents.

### Hint 2 (Cost: 25 points)
> Check the diagnostic capture for ticket **ATL-042**. Engineering implemented a redaction filter, but it was incomplete - some critical request headers were missed.

### Hint 3 (Cost: 50 points)
> Inspect the **`Cookie:`** request header in the trace (`nh_portal_session`). The application accepts this bearer session token directly. Replace your browser's session cookie using DevTools or a replay script to access the Tide-Keeper Vault.

# Review exercise: find the 6 problems

A teammate opened this PR: *"Add endpoint to apply a discount code to an order."*

```csharp
[ApiController]
[Route("api/orders")]
public class OrdersController : ControllerBase
{
    private readonly ShopDbContext _db;
    public OrdersController(ShopDbContext db) => _db = db;

    [HttpPost("{id}/discount")]
    public async Task<IActionResult> ApplyDiscount(int id, string code)
    {
        var order = _db.Orders.FirstOrDefault(o => o.Id == id);

        var discount = _db.Discounts
            .FromSqlRaw("SELECT * FROM Discounts WHERE Code = '" + code + "'")
            .FirstOrDefault();

        try
        {
            order.Total = order.Total - order.Total * discount.Percent / 100;
            foreach (var line in order.Lines)
            {
                line.Product = _db.Products.Find(line.ProductId);
            }
            await _db.SaveChangesAsync();
        }
        catch (Exception)
        {
        }

        return Ok(order);
    }
}
```

Take a few minutes before scrolling.

.

.

.

## Answers

1. **SQL injection (blocking):** the code is concatenated into raw SQL. Use `FromSqlInterpolated` or just LINQ: `_db.Discounts.FirstOrDefaultAsync(d => d.Code == code)`.
2. **No authorization (blocking):** anyone can apply a discount to anyone's order. Add `[Authorize]` and check that the order belongs to the current user.
3. **Null handling:** if the order or the discount does not exist, `order.Total` or `discount.Percent` throws `NullReferenceException`. Return `NotFound()` / `BadRequest()` instead.
4. **Swallowed exception (blocking):** the empty `catch` hides every failure and still returns `200 OK` with possibly unsaved data.
5. **N+1 queries:** `Find` inside the loop hits the database once per line. Use `.Include(o => o.Lines).ThenInclude(l => l.Product)`, or better, don't load products at all since they are not needed here.
6. **Design / business rules:** the discount can be applied again and again (the total keeps dropping), there is no check for expired codes, and the entity is returned directly instead of a DTO. Also `FirstOrDefault` is synchronous in an async method (`FirstOrDefaultAsync`). Ask: should applying a code be idempotent?

Bonus: there are no tests in the PR.

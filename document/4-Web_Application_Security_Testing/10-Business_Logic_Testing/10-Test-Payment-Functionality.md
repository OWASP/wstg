# Test Payment Functionality

|ID          |
|------------|
|WSTG-BUSL-10|

## Summary

Many applications implement payment functionality, including e-commerce sites, subscriptions, charities, donation sites and currency exchanges. The security of this functionality is critical, as vulnerabilities could allow attackers to steal from the organization, make fraudulent purchases, or even to steal payment card details from other users. These issue could result in not only reputational damage to the organization, but also significant financial losses, both from direct losses and fines from industry regulators.

## Test Objectives

- Determine whether the business logic for the e-commerce functionality is robust.
- Understand how the payment functionality works.
- Determine whether the payment functionality is secure.

## How to Test

### Payment Gateway Integration Methods

There are several different ways that applications can integrate payment functionality, and the testing approach will vary depending on which one is used. The most common methods are:

- Redirecting the user to a third-party payment gateway.
- Loading a third-party payment gateway in an IFRAME on the application.
- Having a HTML form that makes a cross-domain POST request to a third-party payment gateway.
- Accepting the card details directly, and then making a POST from the application backend to the payment gateway's API.

### PCI DSS

The Payment Card Industry Data Security Standard (PCI DSS) is a standard that organizations are required to follow in order process debit and card payments (although it's important to note that it is not a law). A full discussion of this standard is outside of the scope of this guide (and of most penetration tests) - but it's useful for testers to understand a few key points.

The most common misconception about PCI DSS is that it only applies to systems that store cardholder data (i.e, debit or credit card details). This is incorrect: it applies to any system that "stores, processes or transmits" this information. Exactly which requirements need to be followed depends on how which of the payment gateway integration methods are used. The [Visa Processing E-Commerce Payments guidance](https://www.visa.co.uk/dam/VCOM/regional/ve/unitedkingdom/PDF/risk/processing-e-commerce-payments-guide-73-17337.pdf) provides further details on this, but as a brief summary:

| Integration Method | Self Assessment Questionnaire (SAQ) |
|--------------------|-------------------------------------|
| Redirect | [SAQ A](https://www.pcisecuritystandards.org/documents/PCI-DSS-v3_2_1-SAQ-A.pdf) |
| IFRAME | [SAQ A](https://www.pcisecuritystandards.org/documents/PCI-DSS-v3_2_1-SAQ-A.pdf) |
| Cross-domain POST | [SAQ A-EP](https://www.pcisecuritystandards.org/documents/PCI-DSS-v3_2-SAQ-A_EP-rev1_1.pdf) |
| Backend API | [SAQ D](https://www.pcisecuritystandards.org/documents/PCI-DSS-v3_2_1-SAQ-D_Merchant.pdf) |

In addition to the differences in the attack surface and risk profile of each approach, there is also a significant difference in the number of requirements between SAQ A (22 requirements) and SAQ D (329 requirements) that the organization needs to meet. As such, it's worth highlighting applications that are not using an redirect or IFRAME, as they represent increased technical and compliance risks.

### Quantity Tampering

Most e-commerce sites allow users to add items to a basket before they start the checkout process. This basket should keep track of which items that have been added, and the quantity of each item. The quantity should normally be a positive integer, but if the site does not properly validate this then it may be possible to specify a decimal quantity of an item (such as `0.1`), or a negative quantity (such as `-1`). Depending on the backend processing, adding negative quantities of an item may result in a negative value, reducing the overall cost of the basket.

There are usually multiple ways to modify the contents of the basket that should be tested, such as:

- Adding a negative quantity of an item.
- Repeatedly removing items until the quantity is negative.
- Updating the quantity to a negative value.

Some sites may also provide a drop-down menu of valid quantities (such as items that must be bought in packs of 10), and it may be possible to tamper these requests to add other quantities of items.

If the full basket details are passed to the payment gateway (rather than simply passing a total value), it may also be possible to tamper the values at that stage.

Finally, if the application is vulnerable to [HTTP parameter pollution](../07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution.md) then it may be possible to cause unexpected behavior by passing a parameter multiple times, such as:

```http
POST /api/basket/add
Host: example.org

item_id=1&quantity=5&quantity=4
```

### Price Tampering

#### On the Application

When adding an item to the basket, the application should only include the item and a quantity, such as the example request below:

```http
POST /api/basket/add HTTP/1.1
Host: example.org

item_id=1&quantity=5
```

However, in some cases the application may also include the price, meaning that it may be possible to tamper it:

```http
POST /api/basket/add HTTP/1.1
Host: example.org

item_id=1&quantity=5&price=2.00
```

Different types of items may have different validation rules, so each type needs to be separately tested. Some applications also allow users to add an optional donation to charity as part of their purchase, and this donation can usually be an arbitrary amount. If this amount is not validated, it may be possible to add a negative donation amount, which would then reduce the total value of the basket.

#### On the Payment Gateway

If the checkout process is performed on a third-party payment gateway, then it may be possible to tamper with the prices between the application and the gateway.

The transfer to the gateway may be performed using a cross-domain POST to the gateway, as shown in the HTML example below.

> Note: The card details are not included in this request - the user will be prompted for them on the payment gateway:

```html
<form action="https://example.org/process_payment" method="POST">
    <input type="hidden" id="merchant_id" value="123" />
    <input type="hidden" id="basket_id" value="456" />
    <input type="hidden" id="item_id" value="1" />
    <input type="hidden" id="item_quantity" value="5" />
    <input type="hidden" id="item_total" value="20.00" />
    <input type="hidden" id="shipping_total" value="2.00" />
    <input type="hidden" id="basket_total" value="22.00" />
    <input type="hidden" id="currency" value="GBP" />
    <input type="submit" id="submit" value="submit" />
</form>
```

By modifying the HTML form or intercepting the POST request, it may be possible to modify the prices of items, and to effectively purchase them for less. Note that many payment gateways will reject a transaction with a value of zero, so a total of 0.01 is more likely to succeed. However, some payment gateways may accept negative values (used to process refunds). Where there are multiple values (such as item prices, a shipping cost, and the total basket cost), all of these should be tested.

If the payment gateway uses an IFRAME instead, it may be possible to perform a similar type of attack by modifying the IFRAME URL:

```html
<iframe src="https://example.org/payment_iframe?merchant_id=123&basket_total=22.00" />
```

> Note: Payment gateways are usually run by a third-parties, and as such may not be included in the scope of testing. This means that while price tampering may be acceptable, other types of attacks (such as SQL injection) should not be performed without explicit written approval).

#### Encrypted Transaction Details

In order to prevent the transaction being tampered with, some payment gateways will encrypt the details of the request that is made to them. For example, [PayPal](https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/encryptedwebpayments/#link-usingewptoprotectmanuallycreatedpaymentbuttons) does this using public key cryptography.

The first thing to try is making an unencrypted request, as some payment gateways allow insecure transactions unless they have been specifically configured to reject them.

If this doesn't work, then you need to find the public key that is used to encrypt the transaction details, which could be exposed in a backup of the application, or if you can find a directory traversal vulnerability.

Alternatively, it's possible that the application re-uses the same public/private key pair for the payment gateway and its digital certificate. You can obtain the public key from the server with the following command:

```bash
echo -e '\0' | openssl s_client -connect example.org:443 2>/dev/null | openssl x509 -pubkey -noout
```

Once you have this key, you can then try and create an encrypted request (based on the payment gateway's documentation), and submit it to the gateway to see if it's accepted.

#### Secure Hashes

Other payment gateways use a secure hash (or a HMAC) of the transaction details to prevent tampering. The exact details of how this is done will vary between providers (for example, [Adyen](https://docs.adyen.com/online-payments/classic-integrations/hosted-payment-pages/hmac-signature-calculation) uses HMAC-SHA256), but it will normally include the details of the transaction and a secret value. For example, a hash may be calculated as:

```php
$secure_hash = md5($merchant_id . $transaction_id . $items . $total_value . $secret)
```

This value is then added to the POST request that is sent to the payment gateway, and verified to ensure that the transaction hasn't been tampered with.

The first thing to try is removing the secure hash, as some payment gateways allow insecure transactions unless a specific configuration option has been set.

The POST request should contain all of the values required to calculate this hash, other than the secret key. This means that if you know how the hash is calculated (which should be included in the payment gateway's documentation), then you can attempt to brute-force the secret. Alternatively, if the site is running an off-the-shelf application, there may be a default secret in the configuration files or source code. Finally, if you can find a backup of the site, or otherwise gain access to the configuration files, you may be able to find the secret there.

If you can obtain this secret, you can then tamper the transaction details, and then generate your own secure hash which will be accepted by the payment gateway.

#### Currency Tampering

If it's not possible to tamper with the actual prices, it may be possible to change the currency that is used, especially where applications support multiple currencies. For example, the application may validate that the price is 10, but if you can change the currency so that you pay 10 USD rather than 10 GBP, this would allow you to purchase items more cheaply.

#### Time Delayed Requests

If the value of items on the site changes over time (for example on a currency exchange), then it may be possible to buy or sell at an old price by intercepting requests using a local proxy and delaying them. In order for this to be exploitable, the price would need to either be included in the request, or linked to something in the request (such as session or transaction ID). The example below shows how this could potentially be exploited on a application that allows users to buy and sell gold:

- View the current price of gold on the site.
- Initiate a buy request for 1oz of gold.
- Intercept and freeze the request.
- Wait one minutes to check the price of gold again:
    - If it increases, allow the transaction to complete, and buy the gold for less than it's current value.
    - If it decreases, drop the request request.

If the site allows the user to make payments using cryptocurrencies (which are usually far more volatile), it may be possible to exploit this by obtaining a fixed price in that cryptocurrency, and then waiting to see if the value rises or falls compared to the main currency used by the site.

### Discount Codes

If the application supports discount codes, then there are various checks that should be carried out:

- Are the codes easily guessable (TEST, TEST10, SORRY, SORRY10, company name, etc)?
    - If a code has a number in, can more codes be found by increasing the number?
- Is there any brute-force protection?
- Can multiple discount codes be applied at once?
- Can discount codes be applied multiple times?
- Can you [inject wildcard characters](../07-Input_Validation_Testing/05-Testing_for_SQL_Injection.md#sql-wildcard-injection) such as `%` or `*`?
- Are discount codes exposed in the HTML source or hidden `<input>` fields anywhere on the application?

In addition to these, the usual vulnerabilities such as SQL injection should be tested for.

### Breaking Payment Flows

If the checkout or payment process on an application involves multiple stages (such as adding items to a basket, entering discount codes, entering shipping details, and entering billing information), then it may be possible to cause unintended behavior by performing these steps outside of the expected sequence. For example, you could try:

- Modifying the shipping address after the billing details have been entered to reduce shipping costs.
- Removing items after entering shipping details, to avoid a minimum basket value.
- Modifying the contents of the basket after applying a discount code.
- Modifying the contents of a basket after completing the checkout process.

It may also be possible to skip the entire payment process for the transaction. For example, if the application redirects to a third-party payment gateway, the payment flow may be:

- The user enters details on the application.
- The user is redirected to the third-party payment gateway.
- The user enters their card details.
    - If the payment is successful, they are redirected to `success.php` on the application.
    - If the payment is unsuccessful, they are redirected to `failure.php` on the application
- The application updates its order database, and processes the order if it was successful.

Depending on whether the application actually validates that the payment on the gateway was successful, it may be possible to force-browse to the `success.php` page (possibly including a transaction ID if one is required), which would cause the site to process the order as though the payment was successful. Additionally, it may be possible to make repeated requests to the `success.php` page to cause an order to be processed multiple times.

### Exploiting Transaction Processing Fees

Merchants normally have to pay fees for every transaction processed, which are typically made up of a small fixed fee, and a percentage of the total value. This means that receiving very small payments (such as $0.01) may result in the merchant actually losing money, as the transaction processing fees are greater than the total value of the transaction.

This issue is rarely exploitable on e-commerce sites, as the price of the cheapest item is usually high enough to prevent it. However, if the site allows customers to make payments with arbitrary amounts (such as donations), check that it enforces a sensible minimum value.

### Test Payment Cards

Most payment gateways have a set of defined test card details, which can be used by developers during testing and debugging. These should only be usable on development or sandbox versions of the gateways, but may be accepted on live sites if they have been misconfigured.

Examples of these test details for various payment gateways are listed below:

- [Adyen - Test Card Numbers](https://docs.adyen.com/development-resources/test-cards/test-card-numbers)
- [Globalpay - Test Cards](https://developer.globalpay.com/resources/test-card-numbers)
- [Stripe - Basic Test Card Numbers](https://stripe.com/docs/testing#cards)
- [Worldpay - Test Card Numbers](http://support.worldpay.com/support/kb/bg/testandgolive/tgl5103.html)

### Testing Logistics

Testing payment functionality on applications can introduce additional complexity, especially if a live site is being tested. Areas that need to be considered include:

- Obtaining test card payment details for the application.
    - If these are not available, then it may be possible to obtain a pre-paid card or an alternative.
- Keeping a record of any orders that are made so that they can be cancelled and refunded.
- Not placing orders that can't be cancelled, or that will cause other actions (such as goods being immediately dispatched from a warehouse).

## Related Test Cases

- [Testing for HTTP Parameter Pollution](../07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution.md)
- [Testing for SQL Injection](../07-Input_Validation_Testing/05-Testing_for_SQL_Injection.md)
- [Testing for the Circumvention of Work Flows](06-Testing_for_the_Circumvention_of_Work_Flows.md)

## Remediation

- Avoid storing, transmitting or processing card details wherever possible.
    - Use a redirect or IFRAME for the payment gateway.
- Review payment gateway documentation and use all available security features (such as encryption and secure hashes).
- Handle all pricing related information on server-side:
    - The only things included in client-side requests should be item IDs and quantities.
- Implement appropriate input validation and business logic constraints (such as checking for negative item numbers or values).
- Ensure that application payment flow is robust and that steps can't be performed out of sequence.

## References

- [Payment Card Industry Data Security Standard (PCI DSS)](https://www.pcisecuritystandards.org/documents/PCI_DSS_v3-2-1.pdf)
- [Visa Processing E-Commerce Payments guidance](https://www.visa.co.uk/dam/VCOM/regional/ve/unitedkingdom/PDF/risk/processing-e-commerce-payments-guide-73-17337.pdf)

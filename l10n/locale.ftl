
invoice-title = Добровольное пожертвование
invoice-description =
    {$starsCount ->
        [one] {$starsCount} звезда
        [few] {$starsCount} звезды
       *[other] {$starsCount} звёзд
}

pre-checkout-failed-reason = Нет больше места для денег 😭

cmd-paysupport =
    Если вы хотите вернуть средства за покупку, воспользуйтесь командой /refund

refund-successful =
    Возврат произведён успешно. Потраченные звёзды уже вернулись на ваш счёт в Telegram.

refund-no-code-provided =
    Пожалуйста, введите команду <code>/refund КОД</code>, где КОД – айди транзакции.
    Его можно увидеть после выполнения платежа, а также в разделе "Звёзды" в приложении Telegram.

refund-code-not-found =
    Такой код покупки не найден. Пожалуйста, проверьте вводимые данные и повторите ещё раз.

refund-already-refunded =
    За эту покупку уже ранее был произведён возврат средств.

payment-successful =
    <b>Огромное спасибо!</b>

    Ваш айди транзакции:
    <code>{$id}</code>

    Сохраните его, если вдруг сделать рефанд в будущем 😢

invoice-link-text =
    Воспользуйтесь <a href="{$link}">этой ссылкой</a> для доната в размере 1 звезды.

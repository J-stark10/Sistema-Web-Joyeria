{% extends "base.html" %}

{% block titulo %}Nueva Compra{% endblock %}

{% block content %}

<form method="POST">

<!-- HEADER -->
<div class="page-header">
    <div>
        <h1 class="page-title">Nueva Compra</h1>
        <p class="page-subtitle">Registro de ingreso de mercadería</p>
    </div>
</div>

<!-- ===================== -->
<!-- LAYOUT 70 / 30 -->
<!-- ===================== -->
<div class="grid grid-cols-1 xl:grid-cols-10 gap-6">

    <!-- ===================== -->
    <!-- 70% MAIN -->
    <!-- ===================== -->
    <div class="xl:col-span-7 space-y-6">

        <!-- PROVEEDOR -->
        <div class="card">

            <div class="card-header">
                <h3 class="card-title">Proveedor</h3>
            </div>

            <select name="id_proveedor" id="proveedor" required>
                <option value="">Seleccione proveedor</option>
                {% for p in proveedores %}
                <option value="{{ p.id_proveedor }}">
                    {{ p.nombre_razon_social }}
                </option>
                {% endfor %}
            </select>

        </div>

        <!-- BUSCADOR -->
        <div class="card">

            <div class="card-header">
                <h3 class="card-title">Buscar Joyas</h3>
            </div>

            <input type="text"
                   id="buscador"
                   placeholder="Buscar por código o nombre...">

            <div id="resultados" class="mt-3"></div>

        </div>

        <!-- DETALLE -->
        <div class="card">

            <div class="card-header">
                <h3 class="card-title">Detalle de Compra</h3>
            </div>

            <div class="table-wrapper">

                <table class="data-table">

                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Joya</th>
                            <th>Stock</th>
                            <th>Costo actual</th>
                            <th>Cant.</th>
                            <th>Costo compra</th>
                            <th>Subtotal</th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody id="detalle-body">

                        <tr id="empty">
                            <td colspan="8" style="text-align:center;padding:2rem;">
                                Sin productos agregados
                            </td>
                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

    </div>

    <!-- ===================== -->
    <!-- 30% RESUMEN -->
    <!-- ===================== -->
    <div class="xl:col-span-3">

        <div class="card sticky top-4">

            <div class="card-header">
                <h3 class="card-title">Resumen de Compra</h3>
            </div>

            <!-- PROVEEDOR INFO -->
            <div class="p-3 rounded-lg mb-4"
                 style="background:var(--color-surface); border:1px solid var(--color-border);">

                <div class="text-sm text-muted">Proveedor seleccionado</div>
                <div id="proveedor-name" class="font-bold">-</div>

            </div>

            <!-- KPIs -->
            <div class="space-y-4">

                <div>
                    <div class="text-sm text-muted">Productos</div>
                    <div id="count" class="text-3xl font-bold">0</div>
                </div>

                <div>
                    <div class="text-sm text-muted">Total</div>
                    <div id="total" class="text-3xl font-bold">Bs 0.00</div>
                </div>

            </div>

            <hr class="my-4">

            <!-- BOTONES -->
            <button type="submit" class="btn btn-primary w-full">
                Registrar Compra
            </button>

            <a href="{{ url_for('compra.index') }}"
               class="btn btn-secondary w-full mt-2">
                Cancelar
            </a>

        </div>

    </div>

</div>

</form>

{% endblock %}



{% block extra_scripts %}
<script>

let joyasMap = new Map();

// ==========================
// PROVEEDOR DISPLAY
// ==========================
const proveedor = document.getElementById("proveedor");

if (proveedor) {
    proveedor.addEventListener("change", () => {

        const text = proveedor.options[proveedor.selectedIndex].text;
        document.getElementById("proveedor-name").innerText = text || "-";

    });
}

// ==========================
// BUSCADOR
// ==========================
const buscador = document.getElementById("buscador");

buscador.addEventListener("input", async () => {

    const q = buscador.value.trim();

    if (q.length < 2) {
        document.getElementById("resultados").innerHTML = "";
        return;
    }

    const res = await fetch(`/compras/buscar-joya?q=${q}`);
    const data = await res.json();

    let html = "";

    data.forEach(j => {

        html += `
            <div class="search-item"
                 style="padding:.6rem;border:1px solid var(--color-border);
                        margin-bottom:.4rem;cursor:pointer;border-radius:8px;"
                 onclick='addJoya(${JSON.stringify(j)})'>

                <strong>${j.codigo}</strong><br>
                ${j.nombre}<br>
                <small>Stock: ${j.stock} | Bs ${j.precio}</small>

            </div>
        `;
    });

    document.getElementById("resultados").innerHTML = html;
});

// ==========================
// AGREGAR JOYA
// ==========================
function addJoya(j) {

    if (joyasMap.has(j.id)) return;

    joyasMap.set(j.id, j);

    document.getElementById("empty")?.remove();

    const tr = document.createElement("tr");

    tr.innerHTML = `
        <td>${j.codigo}
            <input type="hidden" name="id_joya[]" value="${j.id}">
        </td>

        <td>${j.nombre}</td>

        <td>${j.stock}</td>

        <td>Bs ${parseFloat(j.precio).toFixed(2)}</td>

        <td>
            <input type="number"
                   name="cantidad[]"
                   value="1"
                   min="1"
                   oninput="calc()">
        </td>

        <td>
            <input type="number"
                   name="precio[]"
                   value="${j.precio}"
                   step="0.01"
                   oninput="calc()">
        </td>

        <td class="subtotal">Bs 0.00</td>

        <td>
            <button type="button"
                    class="btn btn-danger btn-sm"
                    onclick="removeRow(this, ${j.id})">
                X
            </button>
        </td>
    `;

    document.getElementById("detalle-body").appendChild(tr);

    buscador.value = "";
    document.getElementById("resultados").innerHTML = "";

    calc();
}

// ==========================
// ELIMINAR
// ==========================
function removeRow(btn, id) {

    joyasMap.delete(id);
    btn.closest("tr").remove();

    if (joyasMap.size === 0) {
        document.getElementById("detalle-body").innerHTML = `
            <tr id="empty">
                <td colspan="8" style="text-align:center;padding:2rem;">
                    Sin productos agregados
                </td>
            </tr>
        `;
    }

    calc();
}

// ==========================
// CALCULAR
// ==========================
function calc() {

    let total = 0;

    document.querySelectorAll("#detalle-body tr").forEach(tr => {

        const c = tr.querySelector('input[name="cantidad[]"]');
        const p = tr.querySelector('input[name="precio[]"]');
        const s = tr.querySelector(".subtotal");

        if (!c || !p) return;

        const sub = (parseFloat(c.value) || 0) *
                    (parseFloat(p.value) || 0);

        s.innerText = "Bs " + sub.toFixed(2);

        total += sub;
    });

    document.getElementById("total").innerText = "Bs " + total.toFixed(2);
    document.getElementById("count").innerText = joyasMap.size;
}
</script>

{% endblock %}}

                    <tbody id="detalle-body">

                        <tr id="empty-row">
                            <td colspan="7">
                                <div class="empty-state">
                                    <p>No hay productos agregados</p>
                                    <small>Use el buscador para agregar joyas</small>
                                </div>
                            </td>
                        </tr>

                    </tbody>